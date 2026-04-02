from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime, timezone

# --- Tabela de Usuários ---
class UserAuth(SQLModel, table=True):
    """Dados estritamente para Autenticação e Segurança."""
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True) # Email agora é obrigatório e único
    password: str # Senha simples para o MVP
    role: str = Field(default="user") # 'user' ou 'admin'
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Relação 1:1 com o Perfil
    profile: Optional["UserProfile"] = Relationship(back_populates="auth", sa_relationship_kwargs={"uselist": False})
    # Relações de Histórico
    workouts: List["WorkoutPlan"] = Relationship(back_populates="auth")
    diets: List["DietPlan"] = Relationship(back_populates="auth")

class UserProfile(SQLModel, table=True):
    """Dados Biométricos e Objetivos (Regras de Negócio)."""
    id: Optional[int] = Field(default=None, primary_key=True)
    # Indexado para buscas rápidas de perfil durante o login
    user_auth_id: int = Field(foreign_key="userauth.id", unique=True, index=True)
    nome: str
    idade: int
    peso: float
    altura: int
    genero: str = "masculino"
    frequencia: int = 3
    local: str = "academia"
    objetivo: str
    nivel: str
    dieta: Optional[str] = "onivoro"
    lesoes: Optional[str] = "[]" # Salvaremos como string JSON
    
    # Relação inversa com Auth
    auth: Optional[UserAuth] = Relationship(back_populates="profile")

# --- Tabela de Treinos (Histórico) ---
class WorkoutPlan(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str
    foco: str
    nivel_dificuldade: str
    ai_insight: str # A explicação científica vai aqui
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Relação: Todo treino pertence a um usuário
    # Indexado conforme sugestão do DBA para performance em escala
    user_id: Optional[int] = Field(default=None, foreign_key="userauth.id", index=True)
    auth: Optional[UserAuth] = Relationship(back_populates="workouts")

    # Relação com os exercícios (Normalização)
    exercises: List["WorkoutExercise"] = Relationship(back_populates="workout_plan", sa_relationship_kwargs={"cascade": "all, delete-orphan"})

class WorkoutExercise(SQLModel, table=True):
    """Tabela normalizada de exercícios de um plano."""
    id: Optional[int] = Field(default=None, primary_key=True)
    workout_plan_id: int = Field(foreign_key="workoutplan.id", index=True)
    nome: str
    series: str
    repeticoes: str = "10"
    carga: str = "Moderada"
    descanso: str = "60s"
    ordem: int = 0

    workout_plan: Optional[WorkoutPlan] = Relationship(back_populates="exercises")

# --- Tabela de Logs (Treinos Realizados) ---
class WorkoutLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="userauth.id", index=True)
    workout_plan_id: int = Field(foreign_key="workoutplan.id", index=True)
    data_realizacao: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    duracao_minutos: Optional[int] = None
    esforco_percebido: Optional[int] = None # 1 a 10
    observacoes: Optional[str] = None
    detalhes_json: str # Cargas e reps reais realizadas

# --- Tabela de Logs de Reset de Senha (Segurança) ---
class PasswordResetLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str
    action: str  # "request" ou "confirm"
    status: str  # "success", "failed", "user_not_found"
    ip_address: Optional[str] = None
    user_agent: Optional[str] = Field(max_length=255, default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# --- Tabela de Dietas (Histórico) ---
class DietPlan(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str
    objetivo: str
    restricoes: str  # JSON string com restrições/alergias
    dieta_json: str  # JSON completo da dieta
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    user_id: Optional[int] = Field(default=None, foreign_key="userauth.id", index=True)
    auth: Optional[UserAuth] = Relationship(back_populates="diets")