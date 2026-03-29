from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime, timezone

# --- Tabela de Usuários ---
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    email: str = Field(unique=True, index=True) # Email agora é obrigatório e único
    password: str # Senha simples para o MVP
    idade: int
    peso: float
    altura: int
    genero: str = "masculino"
    frequencia: int = 3
    local: str = "academia"
    objetivo: str
    nivel: str
    dieta: Optional[str] = "onivoro"
    role: str = Field(default="user") # 'user' ou 'admin'
    lesoes: Optional[str] = "[]" # Salvaremos como string JSON
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Relação: Um usuário pode ter vários treinos
    workouts: List["WorkoutPlan"] = Relationship(back_populates="user")
    # Relação: Um usuário pode ter várias dietas
    diets: List["DietPlan"] = Relationship(back_populates="user")

# --- Tabela de Treinos (Histórico) ---
class WorkoutPlan(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str
    foco: str
    nivel_dificuldade: str
    ai_insight: str # A explicação científica vai aqui
    treino_json: str # Vamos salvar o JSON completo dos exercícios aqui por enquanto
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Relação: Todo treino pertence a um usuário
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="workouts")

# --- Tabela de Logs (Treinos Realizados) ---
class WorkoutLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    workout_plan_id: int = Field(foreign_key="workoutplan.id")
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
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="diets")