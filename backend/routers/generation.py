import os
import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from loguru import logger

from backend.database import get_session
from backend.models import User, WorkoutPlan, DietPlan
from backend.schemas import UserCreate, DietRequest
from backend.security import get_current_user, SecurityManager
from backend.services.ai_service import AIService

router = APIRouter()

# Função de dependência para prover o serviço
def get_ai_service():
    return AIService()

@router.post("/gerar-treino", tags=["Geração IA"])
async def gerar_treino(
    perfil: UserCreate, 
    session: Session = Depends(get_session),
    ai_service: AIService = Depends(get_ai_service)
):
    """
    Endpoint de Onboarding: Cria/Atualiza usuário e gera o plano de treino inicial.
    """
    email_normalizado = perfil.email.strip().lower()
    statement = select(User).where(User.email == email_normalizado)
    usuario = session.exec(statement).first()

    # 1. Gerenciar Usuário (Sync com Banco)
    if usuario:
        logger.info(f"🔄 Atualizando perfil existente: {usuario.nome}")
        usuario.peso = perfil.peso
        usuario.objetivo = perfil.objetivo
        usuario.nivel = perfil.nivel
        usuario.frequencia = perfil.frequencia
        usuario.local = perfil.local
        usuario.dieta = perfil.dieta
        usuario.lesoes = json.dumps(perfil.lesoes)
        usuario.password = SecurityManager.hash_password(perfil.password)
    else:
        logger.info(f"✨ Criando novo atleta: {perfil.nome}")
        usuario = User(
            nome=perfil.nome,
            email=email_normalizado,
            password=SecurityManager.hash_password(perfil.password),
            idade=perfil.idade,
            peso=perfil.peso,
            altura=perfil.altura,
            objetivo=perfil.objetivo,
            nivel=perfil.nivel,
            genero=perfil.genero,
            frequencia=perfil.frequencia,
            local=perfil.local,
            dieta=perfil.dieta,
            lesoes=json.dumps(perfil.lesoes)
        )
    
    session.add(usuario)
    session.commit()
    session.refresh(usuario)

    # 2. Lógica de Geração de Treino
    treino_final = None

    # Se o usuário escolheu exercícios manualmente no Passo 6
    if perfil.exercicios and len(perfil.exercicios) > 0:
        logger.info("🛠️ Usando seleção manual de exercícios.")
        treino_final = {
            "titulo": f"Treino de {usuario.nome}",
            "foco": perfil.objetivo,
            "intensidade": "Personalizada",
            "ai_insight": "Plano montado com base na sua seleção manual. Foco na execução!",
            "exercicios": perfil.exercicios
        }
    else:
        # Delegamos a chamada ao serviço especializado
        treino_final = await ai_service.generate_workout(usuario.nome, perfil.dict())

    if not treino_final:
        raise HTTPException(status_code=502, detail="A IA não conseguiu gerar o treino no momento.")

    # 3. Salvar Plano de Treino
    novo_plano = WorkoutPlan(
        user_id=usuario.id,
        titulo=treino_final.get("titulo", "Treino Personalizado"),
        foco=treino_final.get("foco", perfil.objetivo),
        nivel_dificuldade=treino_final.get("intensidade", "Média"),
        ai_insight=treino_final.get("ai_insight", "Análise IA"),
        treino_json=json.dumps(treino_final.get("exercicios", []))
    )
    session.add(novo_plano)
    session.commit()
    session.refresh(novo_plano)

    return {
        "status": "sucesso",
        "user_id": usuario.id,
        "treino_id": novo_plano.id,
        "treino": treino_final
    }

@router.post("/gerar-dieta", tags=["Geração IA"])
async def gerar_dieta(
    dados: DietRequest, 
    current_user: User = Depends(get_current_user), 
    session: Session = Depends(get_session),
    ai_service: AIService = Depends(get_ai_service)
):
    """
    Gera um plano alimentar baseado no perfil do usuário autenticado.
    """
    if current_user.id != dados.user_id:
        raise HTTPException(status_code=403, detail="Acesso negado para este perfil.")

    logger.info(f"🥗 Gerando dieta para: {current_user.nome}")
    
    dieta_data = await ai_service.generate_diet(current_user.dict(), dados.dict())

    if not dieta_data:
        raise HTTPException(status_code=502, detail="Falha ao gerar dieta com a IA.")

    nova_dieta = DietPlan(
        titulo=f"Dieta para {current_user.nome}",
        objetivo=dados.objetivo,
        restricoes=json.dumps(dados.restricoes),
        dieta_json=json.dumps(dieta_data),
        user_id=current_user.id
    )
    session.add(nova_dieta)
    session.commit()
    session.refresh(nova_dieta)

    return {"status": "sucesso", "dieta": dieta_data, "dieta_id": nova_dieta.id}