import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from backend.database import get_session
from backend.models import User, WorkoutPlan, DietPlan
from backend.schemas import UserUpdate, ChangePasswordRequest
from backend.security import get_current_user, SecurityManager

router = APIRouter()

@router.get("/dashboard/me")
def get_user_dashboard(
    current_user: User = Depends(get_current_user), 
    session: Session = Depends(get_session)
):
    """Retorna os dados consolidados para o dashboard do atleta logado."""
    user_id = current_user.id
    
    # Busca o último treino e última dieta registrados
    ultimo_treino = session.exec(
        select(WorkoutPlan)
        .where(WorkoutPlan.user_id == user_id)
        .order_by(WorkoutPlan.created_at.desc())
    ).first()
    
    ultima_dieta = session.exec(
        select(DietPlan)
        .where(DietPlan.user_id == user_id)
        .order_by(DietPlan.created_at.desc())
    ).first()

    return {
        "user": current_user,
        "treino": {
            "titulo": ultimo_treino.titulo,
            "foco": ultimo_treino.foco,
            "intensidade": ultimo_treino.nivel_dificuldade,
            "ai_insight": ultimo_treino.ai_insight,
            "exercicios": json.loads(ultimo_treino.treino_json)
        } if ultimo_treino else None,
        "treino_meta": ultimo_treino,
        "dieta": json.loads(ultima_dieta.dieta_json) if ultima_dieta else None
    }

@router.put("/{user_id}")
def atualizar_perfil(
    user_id: int, 
    dados: UserUpdate, 
    current_user: User = Depends(get_current_user), 
    session: Session = Depends(get_session)
):
    """Atualiza dados biométricos e objetivos do perfil do atleta."""
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Você não tem permissão para editar este perfil")

    update_data = dados.dict(exclude_unset=True)
    
    # Proteção de integridade: Impede alteração de campos sistêmicos via esta rota
    campos_bloqueados = ["id", "email", "role", "created_at", "password"]
    for key, value in update_data.items():
        if key not in campos_bloqueados:
            setattr(current_user, key, value)
    
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    
    return {"status": "sucesso", "usuario": current_user}

@router.put("/{user_id}/password")
def atualizar_senha(
    user_id: int, 
    dados: ChangePasswordRequest, 
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Realiza a troca de senha validando a credencial anterior."""
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Operação não autorizada")
    
    if not SecurityManager.verify_password(dados.old_password, current_user.password):
        raise HTTPException(status_code=400, detail="Senha atual incorreta")
    
    current_user.password = SecurityManager.hash_password(dados.new_password)
    session.add(current_user)
    session.commit()
    
    return {"status": "sucesso", "mensagem": "Senha alterada com sucesso!"}