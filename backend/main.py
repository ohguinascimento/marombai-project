import re # <--- Importante para limpar os textos
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
from backend.database import create_db_and_tables, get_session
from backend.models import User
from pydantic import BaseModel
from typing import List
import httpx


# --- "Vida" do App ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

# --- CORS ---
origins = ["http://localhost:5173", "http://127.0.0.1:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Modelo de Entrada ---
class UserProfile(BaseModel):
    nome: str
    idade: str
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

# --- Função Auxiliar de Limpeza ---
def limpar_numero(valor: str) -> float:
    """
    Converte string para numero.
    Ex: '1,80' -> 1.80
    Ex: '80kg' -> 80.0
    """
    if not valor:
        return 0
    
    # 1. Troca vírgula por ponto (Brasil -> Code)
    valor_formatado = str(valor).replace(',', '.')
    
    # 2. Mantém apenas números e pontos
    numeros = re.sub(r'[^0-9.]', '', valor_formatado)
    
    if not numeros:
        return 0
    
    return float(numeros)

def ajustar_altura(valor: str) -> int:
    """Detecta se é metros ou cm e padroniza para cm"""
    numero = limpar_numero(valor)
    # Se for menor que 3 (ex: 1.80), assume que é metros e converte
    if numero < 3.0:
        return int(numero * 100)
    return int(numero)

# --- Rota Principal ---
@app.post("/gerar-treino")
async def gerar_treino(profile: UserProfile, session: Session = Depends(get_session)):
    # Nota: mudei 'def' para 'async def' para usar o httpx
    print(f"Recebi dados: {profile.nome} | Objetivo: {profile.objetivo}")
    
    try:
        # 1. SALVAR NO BANCO
        novo_usuario = User(
            nome=profile.nome,
            idade=int(limpar_numero(profile.idade)),
            peso=float(limpar_numero(profile.peso)),
            altura=ajustar_altura(profile.altura),
            objetivo=profile.objetivo,
            nivel=profile.nivel
        )
        
        session.add(novo_usuario)
        session.commit()
        session.refresh(novo_usuario)
        print(f"✅ Usuário salvo! ID: {novo_usuario.id}")

        # 2. CHAMAR O N8N (O CÉREBRO)
        # URL do Webhook de TESTE (copiado do n8n)
        webhook_url = "http://localhost:5678/webhook-test/gerar-treino"
        
        # Preparar os dados para enviar pro n8n
        payload = {
            "usuario_id": novo_usuario.id,
            "nome": novo_usuario.nome,
            "perfil": {
                "idade": novo_usuario.idade,
                "peso": novo_usuario.peso,
                "altura": novo_usuario.altura,
                "objetivo": novo_usuario.objetivo,
                "nivel": novo_usuario.nivel,
                "lesoes": profile.lesoes,
                "restricoes": profile.restricoes
            }
        }

        print("Enviando para o n8n...")
        
        # O timeout é alto (30s) porque a IA demora para pensar
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(webhook_url, json=payload)
        
        print(f"Resposta do n8n: {response.status_code}")

        # Se o n8n responder sucesso, devolvemos o JSON dele pro Front
        if response.status_code == 200:
            dados_n8n = response.json()
            # Por enquanto, se o n8n devolver só mensagem, usamos o mock de treino como fallback
            # para não quebrar o front, até configurarmos a IA completa.
            return {
                "status": "sucesso",
                "mensagem": "Treino gerado pela IA (Simulação)",
                "treino": dados_n8n.get("treino", { 
                    # FALLBACK SE O N8N NÃO MANDAR O TREINO COMPLETO AINDA
                    "titulo": f"Treino IA de {novo_usuario.nome}",
                    "foco": novo_usuario.objetivo,
                    "aiInsight": "Conexão com n8n estabelecida! Configure a OpenAI agora.",
                    "exercicios": []
                })
            }
        else:
             return {"status": "erro", "mensagem": "O n8n não respondeu corretamente."}

    except Exception as e:
        print(f"❌ ERRO: {e}")
        return {"status": "erro", "mensagem": f"Erro interno: {str(e)}"}