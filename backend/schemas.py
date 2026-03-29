from pydantic import BaseModel, EmailStr
from typing import List, Optional

class UserCreate(BaseModel):
    nome: str
    email: EmailStr
    password: str
    idade: int
    peso: float
    altura: int
    objetivo: str
    nivel: str
    genero: str = "masculino"
    lesoes: List[str] = []
    restricoes: List[str] = []
    frequencia: int
    local: str
    dieta: str
    suplementos: List[str] = []
    exercicios: List[dict] = []

class UserUpdate(BaseModel):
    nome: Optional[str] = None
    idade: Optional[int] = None
    peso: Optional[float] = None
    altura: Optional[int] = None
    objetivo: Optional[str] = None
    nivel: Optional[str] = None
    frequencia: Optional[int] = None
    local: Optional[str] = None
    dieta: Optional[str] = None

class WorkoutUpdate(BaseModel):
    titulo: Optional[str] = None
    foco: Optional[str] = None
    nivel_dificuldade: Optional[str] = None
    ai_insight: Optional[str] = None
    exercicios: List[dict]

class WorkoutLogCreate(BaseModel):
    user_id: int
    workout_plan_id: int
    duracao_minutos: int
    esforco_percebido: int
    detalhes_exercicios: List[dict]

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordResetConfirmRequest(BaseModel):
    token: str
    new_password: str

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

class DietRequest(BaseModel):
    user_id: int
    objetivo: str
    restricoes: list = []
    preferencias: list = []
    dieta: str = "onivoro"
    suplementos: list = []

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str