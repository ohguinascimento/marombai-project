import os
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from loguru import logger

from backend.database import get_session
from backend.models import User, WorkoutPlan, DietPlan, PasswordResetLog
from backend.security import get_current_admin

router = APIRouter()

@router.get("/usuarios", response_model=List[User])
def listar_usuarios(session: Session = Depends(get_session), admin: User = Depends(get_current_admin)):
    """Lista todos os atletas cadastrados na plataforma."""
    return session.exec(select(User)).all()

@router.get("/treinos")
def listar_treinos(session: Session = Depends(get_session), admin: User = Depends(get_current_admin)):
    """Lista todos os planos de treino gerados pelo sistema."""
    return session.exec(select(WorkoutPlan)).all()

@router.get("/dietas")
def listar_dietas(session: Session = Depends(get_session), admin: User = Depends(get_current_admin)):
    """Lista todos os planos de dieta gerados pelo sistema."""
    return session.exec(select(DietPlan)).all()

@router.get("/security-logs", response_model=List[PasswordResetLog])
def listar_logs_seguranca(session: Session = Depends(get_session), admin: User = Depends(get_current_admin)):
    """Retorna o histórico de tentativas de reset de senha para auditoria."""
    return session.exec(select(PasswordResetLog).order_by(PasswordResetLog.created_at.desc())).all()

@router.get("/logs/files")
def listar_arquivos_logs(admin: User = Depends(get_current_admin)):
    """Lista os arquivos de log físicos gerados pelo Loguru no servidor."""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        return []
    # Filtra apenas arquivos .log e ordena pelo mais recente
    files = [f for f in os.listdir(log_dir) if f.endswith(".log")]
    return sorted(files, reverse=True)

@router.get("/logs/view/{filename}")
def ler_conteudo_log(filename: str, admin: User = Depends(get_current_admin)):
    """Lê as últimas 1000 linhas de um arquivo de log específico com proteção de path traversal."""
    # Previne que o usuário tente ler arquivos fora da pasta /logs
    clean_filename = os.path.basename(filename)
    log_path = os.path.join("logs", clean_filename)
    
    if not os.path.exists(log_path):
        raise HTTPException(status_code=404, detail="Arquivo de log não encontrado.")
    
    try:
        with open(log_path, "r", encoding="utf-8") as f:
            # Retornamos apenas o final do arquivo para performance
            lines = f.readlines()[-1000:]
        return {"filename": clean_filename, "content": "".join(lines)}
    except Exception as e:
        logger.error(f"Erro ao ler arquivo de log {clean_filename}: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao processar o arquivo.")