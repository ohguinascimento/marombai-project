import os
import httpx
from datetime import datetime, timezone
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session, select
from loguru import logger
from jose import jwt, exceptions

from backend.database import get_session
from backend.models import UserAuth, PasswordResetLog
from backend.schemas import LoginRequest, PasswordResetRequest, PasswordResetConfirmRequest, Token
from backend.security import SecurityManager, SECRET_KEY, ALGORITHM

router = APIRouter()

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

async def send_sendgrid_email(to_email: str, subject: str, html_content: str):
    """Função auxiliar para envio de e-mail via SendGrid."""
    api_key = os.getenv("SENDGRID_API_KEY")
    if not api_key:
        logger.warning(f"⚠️ SENDGRID_API_KEY ausente. SIMULAÇÃO DE E-MAIL para {to_email}")
        logger.info(f"🔗 LINK DE RECUPERAÇÃO GERADO: \n\n {html_content} \n")
        return True

    url = "https://api.sendgrid.com/v3/mail/send"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "personalizations": [{"to": [{"email": to_email}]}],
        "from": {"email": "suporte@marombai.app", "name": "MarombAI Support"},
        "subject": subject,
        "content": [{"type": "text/html", "value": html_content}]
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        return response.status_code == 202

@router.post("/login", response_model=Any)
def login(dados: LoginRequest, session: Session = Depends(get_session)):
    email_normalizado = dados.email.strip().lower()
    logger.info(f"🔑 Tentativa de login para: {email_normalizado}")
    
    # Eagerly load the profile to avoid AttributeError when accessing user.profile
    from sqlalchemy.orm import selectinload
    user = session.exec(
        select(UserAuth).options(selectinload(UserAuth.profile))
        .where(UserAuth.email == email_normalizado)
    ).first()
    
    if not user or not SecurityManager.verify_password(dados.password, user.password):
        logger.warning(f"❌ [LOGIN] Falha para '{email_normalizado}'. Credenciais inválidas.")
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")

    logger.info(f"✅ [LOGIN] Sucesso: Usuário ID {user.id}")
    
    # Agora o token carrega informações básicas para o Frontend e para validações rápidas no Backend
    token_data = {
        "sub": str(user.id),
        "nome": user.profile.nome if user.profile else "Atleta",
        "role": user.role
    }
    
    access_token = SecurityManager.create_access_token(data=token_data)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {"id": user.id, "nome": token_data["nome"], "role": user.role}
    }

@router.post("/reset-password")
async def request_password_reset(dados: PasswordResetRequest, request: Request, session: Session = Depends(get_session)):
    """Inicia o fluxo de reset enviando o e-mail com token."""
    email_normalizado = dados.email.strip().lower()
    ip = request.client.host
    ua = request.headers.get("user-agent", "")[:255]

    user = session.exec(select(UserAuth).where(UserAuth.email == email_normalizado)).first()
    
    if not user:
        log = PasswordResetLog(email=email_normalizado, action="request", status="user_not_found", ip_address=ip, user_agent=ua)
        session.add(log)
        session.commit()
        return {"status": "sucesso", "mensagem": "Se o e-mail existir, um link de recuperação foi enviado."}
    
    token = SecurityManager.create_password_reset_token(email_normalizado)
    reset_link = f"{FRONTEND_URL}/reset-password/confirm?token={token}"
    
    nome_usuario = user.profile.nome if user.profile else "Marombeiro"
    html = f"<p>Olá {nome_usuario},</p><p>Clique no link abaixo para resetar sua senha:</p><a href='{reset_link}'>{reset_link}</a>"
    await send_sendgrid_email(email_normalizado, "Recuperação de Senha - MarombAI", html)
    
    log = PasswordResetLog(email=email_normalizado, action="request", status="success", ip_address=ip, user_agent=ua)
    session.add(log)
    session.commit()

    return {"status": "sucesso", "mensagem": "E-mail de recuperação enviado."}

@router.post("/reset-password/confirm")
def confirm_password_reset(dados: PasswordResetConfirmRequest, request: Request, session: Session = Depends(get_session)):
    """Valida o token e define a nova senha."""
    ip = request.client.host
    ua = request.headers.get("user-agent", "")[:255]
    email_log = "unknown"

    try:
        payload = jwt.decode(dados.token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("purpose") != "password_reset":
            raise HTTPException(status_code=400, detail="Token inválido para esta operação")
        email_log = payload.get("sub")
    except exceptions.ExpiredSignatureError:
        log = PasswordResetLog(email=email_log, action="confirm", status="expired", ip_address=ip, user_agent=ua)
        session.add(log)
        session.commit()
        raise HTTPException(status_code=400, detail="O link de recuperação expirou.")
    except jwt.JWTError as e:
        logger.error(f"❌ Erro na validação do token: {str(e)}")
        raise HTTPException(status_code=400, detail="Link de recuperação inválido.")

    user = session.exec(select(UserAuth).where(UserAuth.email == email_log)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    user.password = SecurityManager.hash_password(dados.new_password)
    log = PasswordResetLog(email=email_log, action="confirm", status="success", ip_address=ip, user_agent=ua)
    session.add(log)
    session.add(user)
    session.commit()
    
    return {"status": "sucesso", "mensagem": "Senha atualizada com sucesso!"}