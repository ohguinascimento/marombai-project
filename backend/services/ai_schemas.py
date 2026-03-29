from pydantic import BaseModel, Field, validator
from typing import List, Optional

class UserDataSchema(BaseModel):
    nome: str = Field(..., min_length=2)
    peso: float = Field(..., gt=0, lt=500)
    altura: Optional[float] = Field(None, gt=0, lt=300)
    idade: Optional[int] = Field(None, gt=0, lt=120)

class DietProfileSchema(BaseModel):
    objetivo: str
    dieta: str  # Ex: "Onívora", "Vegana"
    restricoes: List[str] = Field(default_factory=list)

    @validator('objetivo')
    def validar_objetivo(cls, v):
        permitidos = ["Hipertrofia", "Emagrecimento", "Manutenção", "Performance"]
        if v not in permitidos:
            raise ValueError(f"Objetivo deve ser um de: {permitidos}")
        return v

class WorkoutProfileSchema(BaseModel):
    objetivo: str
    nivel: str = "Iniciante"  # Iniciante, Intermediário, Avançado
    frequencia: int = Field(3, ge=1, le=7)
    limitacoes: List[str] = Field(default_factory=list)

class AIResponseSchema(BaseModel):
    """Modelo para validar o que volta do n8n (opcional)"""
    sucesso: bool = True
    resultado: Optional[dict] = None