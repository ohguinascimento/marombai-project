import json
from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from loguru import logger

from backend.database import get_session
from backend.models import User, WorkoutPlan, WorkoutLog
from backend.schemas import WorkoutUpdate, WorkoutLogCreate
from backend.security import get_current_user

router = APIRouter()

# --- Biblioteca de Treinos Pré-cadastrados (Templates) ---
TREINOS_TEMPLATES = [
    {
        "id": 1,
        "titulo": "Adaptação Full Body",
        "foco": "Corpo Inteiro",
        "intensidade": "Iniciante",
        "ai_insight": "Foco em técnica e adaptação neuromuscular para quem está começando.",
        "exercicios": [
            {"nome": "Leg Press 45", "series": "3x15", "carga": "Leve", "descanso": "60s"},
            {"nome": "Puxada Alta", "series": "3x15", "carga": "Leve", "descanso": "60s"},
            {"nome": "Supino Máquina", "series": "3x15", "carga": "Leve", "descanso": "60s"},
            {"nome": "Abdominal Supra", "series": "3x20", "carga": "Peso Corporal", "descanso": "45s"}
        ]
    },
    {
        "id": 2,
        "titulo": "Push (Empurrar) - Hipertrofia",
        "foco": "Peito, Ombro e Tríceps",
        "intensidade": "Intermediário",
        "ai_insight": "Foco em exercícios de empurrar com cadência controlada.",
        "exercicios": [
            {"nome": "Supino Inclinado Halter", "series": "4x10", "carga": "Moderada", "descanso": "90s"},
            {"nome": "Desenvolvimento Militar", "series": "3x10", "carga": "Moderada", "descanso": "90s"},
            {"nome": "Tríceps Testa", "series": "3x12", "carga": "Moderada", "descanso": "60s"},
            {"nome": "Elevação Lateral", "series": "4x15", "carga": "Leve", "descanso": "45s"}
        ]
    },
    {
        "id": 3,
        "titulo": "Pull (Puxar) - Costas e Bíceps",
        "foco": "Costas e Bíceps",
        "intensidade": "Intermediário",
        "ai_insight": "Trabalho focado em tração para densidade das costas.",
        "exercicios": [
            {"nome": "Remada Curvada", "series": "4x10", "carga": "Moderada", "descanso": "90s"},
            {"nome": "Puxada Aberta", "series": "3x12", "carga": "Moderada", "descanso": "60s"},
            {"nome": "Rosca Direta W", "series": "3x10", "carga": "Moderada", "descanso": "60s"},
            {"nome": "Crucifixo Inverso", "series": "3x15", "carga": "Leve", "descanso": "45s"}
        ]
    }
]

@router.get("/templates")
def listar_templates():
    """Retorna a biblioteca de treinos pré-definidos."""
    return TREINOS_TEMPLATES

@router.post("/select-template/{template_id}")
def selecionar_treino_template(
    template_id: int, 
    current_user: User = Depends(get_current_user), 
    session: Session = Depends(get_session)
):
    """Aplica um treino pré-definido ao perfil do usuário autenticado."""
    template = next((t for t in TREINOS_TEMPLATES if t["id"] == template_id), None)
    if not template:
        raise HTTPException(status_code=404, detail="Template de treino não encontrado")
    
    novo_plano = WorkoutPlan(
        user_id=current_user.id,
        titulo=template["titulo"],
        foco=template["foco"],
        nivel_dificuldade=template["intensidade"],
        ai_insight=template["ai_insight"],
        treino_json=json.dumps(template["exercicios"])
    )
    
    session.add(novo_plano)
    session.commit()
    session.refresh(novo_plano)
    return {"status": "sucesso", "mensagem": "Treino aplicado!", "treino": template}

@router.put("/{workout_id}")
def atualizar_treino(
    workout_id: int, 
    dados: WorkoutUpdate, 
    current_user: User = Depends(get_current_user), 
    session: Session = Depends(get_session)
):
    """Atualiza um plano de treino existente validando a propriedade."""
    workout = session.get(WorkoutPlan, workout_id)
    if not workout:
        raise HTTPException(status_code=404, detail="Treino não encontrado")
    
    if workout.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Acesso negado: Este treino não pertence a você")

    if dados.titulo: workout.titulo = dados.titulo
    if dados.foco: workout.foco = dados.foco
    if dados.nivel_dificuldade: workout.nivel_dificuldade = dados.nivel_dificuldade
    if dados.ai_insight: workout.ai_insight = dados.ai_insight
    
    workout.treino_json = json.dumps(dados.exercicios)
    
    session.add(workout)
    session.commit()
    session.refresh(workout)
    return {"status": "sucesso", "treino": json.loads(workout.treino_json), "meta": workout}

@router.post("/finish")
def finalizar_treino(
    dados: WorkoutLogCreate, 
    current_user: User = Depends(get_current_user), 
    session: Session = Depends(get_session)
):
    """Registra a conclusão de uma sessão de treino."""
    if current_user.id != dados.user_id:
        raise HTTPException(status_code=403, detail="Não é permitido salvar treinos para outro usuário")

    novo_log = WorkoutLog(
        user_id=dados.user_id,
        workout_plan_id=dados.workout_plan_id,
        duracao_minutos=dados.duracao_minutos,
        esforco_percebido=dados.esforco_percebido,
        detalhes_json=json.dumps(dados.detalhes_exercicios)
    )
    session.add(novo_log)
    session.commit()
    return {"status": "sucesso", "log_id": novo_log.id}

@router.get("/evolution")
def get_user_evolution(
    current_user: User = Depends(get_current_user), 
    session: Session = Depends(get_session)
):
    """Busca o histórico de treinos do usuário logado."""
    statement = select(WorkoutLog).where(WorkoutLog.user_id == current_user.id).order_by(WorkoutLog.data_realizacao.asc())
    logs = session.exec(statement).all()

    return [
        {
            "id": log.id,
            "data": log.data_realizacao.strftime("%d/%m"),
            "duracao": log.duracao_minutos,
            "esforco": log.esforco_percebido,
            "observacoes": log.observacoes,
            "exercicios": json.loads(log.detalhes_json) if log.detalhes_json else []
        } for log in logs
    ]