from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional

app = FastAPI()

# --- CONFIGURAÇÃO DE SEGURANÇA (CORS) ---
# Aqui liberamos o React (http://localhost:5173) para falar com o Python
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MODELO DE DADOS (O Contrato) ---
# Isso garante que o Python só aceite se os dados vierem certinhos
class UserProfile(BaseModel):
    nome: str
    idade: str
    genero: str
    peso: str
    altura: str
    objetivo: str
    nivel: str
    frequencia: int
    local: str
    lesoes: List[str]
    restricoes: List[str]
    dieta: str
    suplementos: List[str]

# --- ROTA DE CRIAÇÃO DE TREINO ---
@app.post("/gerar-treino")
def gerar_treino(user: UserProfile):
    def gerar_treino(user: UserProfile):
        print(f"Recebi dados: {user.nome} | Objetivo: {user.objetivo}")
    
    # MOCK MAIS COMPLEXO (Simulando o que a IA vai gerar depois)
    # Aqui estamos devolvendo dados dinâmicos baseados no nome do usuário
    return {
        "status": "sucesso",
        "mensagem": "Treino gerado via Python!",
        "treino": {
            "titulo": f"Treino do {user.nome}", # <--- Dinâmico!
            "foco": user.objetivo.capitalize(), # <--- Dinâmico!
            "duracao": "60 min",
            "intensidade": "Insana",
            "xp": 1000,
            "aiInsight": f"Como você citou {user.objetivo}, foquei em volume alto hoje. Cuidado com o descanso!",
            "exercicios": [
                {
                    "id": 1,
                    "nome": "Supino Reto (Python Edition)", # <--- Prova que veio do back
                    "series": "4x10",
                    "carga": "PRO",
                    "img": "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=400&q=80"
                },
                {
                    "id": 2,
                    "nome": "Agachamento Hack",
                    "series": "3x12",
                    "carga": "50kg",
                    "img": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=400&q=80"
                }
            ]
        }
    }
    
    # AQUI VAI ENTRAR A IA DEPOIS
    # Por enquanto, vamos devolver um "OK" falso só pra testar a conexão
    
    

@app.get("/")
def home():
    return {"message": "MarombAI Backend está ON!"}