import os
import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from loguru import logger

from backend.database import get_session
from backend.models import UserAuth, UserProfile, WorkoutPlan, WorkoutExercise, DietPlan
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
    # Eagerly load the profile to avoid AttributeError when accessing auth.profile
    from sqlalchemy.orm import selectinload
    auth = session.exec(
        select(UserAuth).options(selectinload(UserAuth.profile))
        .where(UserAuth.email == email_normalizado)
    ).first()

    # 1. Gerenciar Usuário (Sync com Banco)
    if auth:
        logger.info(f"🔄 Atualizando credenciais de: {auth.email}")
        auth.password = SecurityManager.hash_password(perfil.password)
        if auth.profile:
            auth.profile.peso = perfil.peso
            auth.profile.objetivo = perfil.objetivo
            auth.profile.nivel = perfil.nivel
            auth.profile.frequencia = perfil.frequencia
            auth.profile.lesoes = json.dumps(perfil.lesoes)
    else:
        logger.info(f"✨ Criando novo atleta: {perfil.nome}")
        auth = UserAuth(
            email=email_normalizado,
            password=SecurityManager.hash_password(perfil.password),
        )
        session.add(auth)
        session.flush() # Gera ID para o Auth

        profile = UserProfile(
            user_auth_id=auth.id,
            nome=perfil.nome,
            idade=perfil.idade,
            peso=perfil.peso,
            altura=perfil.altura,
            genero=perfil.genero,
            frequencia=perfil.frequencia,
            local=perfil.local,
            dieta=perfil.dieta,
            lesoes=json.dumps(perfil.lesoes)
        )
        session.add(profile)

    session.add(auth)
    session.commit()
    session.refresh(auth)

    # 2. Lógica de Geração de Treino
    treino_final = None

    # Se o usuário escolheu exercícios manualmente no Passo 6
    if perfil.exercicios and len(perfil.exercicios) > 0:
        logger.info("🛠️ Usando seleção manual de exercícios.")
        treino_final = {
            "titulo": f"Treino de {perfil.nome}",
            "foco": perfil.objetivo,
            "intensidade": "Personalizada",
            "ai_insight": "Plano montado com base na sua seleção manual. Foco na execução!",
            "exercicios": perfil.exercicios
        }
    else:
        # Delegamos a chamada ao serviço especializado
        treino_final = await ai_service.generate_workout(perfil.nome, perfil.dict())

    if not treino_final:
        raise HTTPException(status_code=502, detail="A IA não conseguiu gerar o treino no momento.")

    # 3. Salvar Plano de Treino
    novo_plano = WorkoutPlan(
        user_id=auth.id,
        titulo=treino_final.get("titulo", "Treino Personalizado"),
        foco=treino_final.get("foco", perfil.objetivo),
        nivel_dificuldade=treino_final.get("intensidade", "Média"),
        ai_insight=treino_final.get("ai_insight", "Análise IA"),
    )
    session.add(novo_plano)
    session.flush() # Flush para obter o ID do plano sem fechar a transação

    # 4. Salvar Exercícios individualmente (Normalização)
    lista_exercicios = treino_final.get("exercicios", [])
    for i, ex in enumerate(lista_exercicios):
        exercicio_db = WorkoutExercise(
            workout_plan_id=novo_plano.id,
            nome=ex.get("nome"),
            series=ex.get("series"),
            repeticoes=ex.get("repeticoes") or ex.get("series").split("x")[-1], # Fallback simples
            carga=ex.get("carga", "Moderada"),
            descanso=ex.get("descanso", "60s"),
            ordem=i
        )
        session.add(exercicio_db)

    session.commit()
    session.refresh(novo_plano)

    return {
        "status": "sucesso",
        "user_id": auth.id,
        "treino_id": novo_plano.id,
        "treino": treino_final
    }

@router.post("/gerar-dieta", tags=["Geração IA"])
async def gerar_dieta(
    dados: DietRequest, 
    current_user: UserAuth = Depends(get_current_user), 
    session: Session = Depends(get_session),
    ai_service: AIService = Depends(get_ai_service)
):
    """
    Gera um plano alimentar baseado no perfil do usuário autenticado.
    """
    if current_user.id != dados.user_id:
        raise HTTPException(status_code=403, detail="Acesso negado para este perfil.")

    nome_usuario = current_user.profile.nome if current_user.profile else "Atleta"
    logger.info(f"🥗 Gerando dieta para: {nome_usuario}")
    
    dieta_data = await ai_service.generate_diet(current_user.dict(), dados.dict())

    if not dieta_data:
        raise HTTPException(status_code=502, detail="Falha ao gerar dieta com a IA.")

    nome_user = current_user.profile.nome if current_user.profile else "Atleta"
    nova_dieta = DietPlan(
        titulo=f"Dieta para {nome_user}",
        objetivo=dados.objetivo,
        restricoes=json.dumps(dados.restricoes),
        dieta_json=json.dumps(dieta_data),
        user_id=current_user.id
    )
    session.add(nova_dieta)
    session.commit()
    session.refresh(nova_dieta)

    return {"status": "sucesso", "dieta": dieta_data, "dieta_id": nova_dieta.id}