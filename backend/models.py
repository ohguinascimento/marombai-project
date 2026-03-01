from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime

# --- Tabela de Usuários ---
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    email: Optional[str] = None
    idade: int
    peso: float
    altura: int
    objetivo: str
    nivel: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
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
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relação: Todo treino pertence a um usuário
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="workouts")

# --- Tabela de Dietas (Histórico) ---
class DietPlan(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str
    objetivo: str
    restricoes: str  # JSON string com restrições/alergias
    dieta_json: str  # JSON completo da dieta
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="diets")