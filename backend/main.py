# --- BIBLIOTECAS EXTERNAS ---
import json
import httpx
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware 
from sqlmodel import Session, select
from contextlib import asynccontextmanager
from typing import List, Optional
from pydantic import BaseModel
import os

# --- ARQUIVOS LOCAIS ---
from backend.database import get_session, init_db
from backend.models import User, WorkoutPlan, DietPlan

# --- Modelos de Entrada (Pydantic) ---
class UserCreate(BaseModel):
    nome: str
    email: str
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

class DietRequest(BaseModel):
    user_id: int
    objetivo: str
    restricoes: list = []
    preferencias: list = []
    dieta: str = "onivoro"
    suplementos: list = []

class LoginRequest(BaseModel):
    email: str
    password: str

# --- Ciclo de Vida ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

# --- CONFIGURAÇÃO DO CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ROTAS ---

@app.get("/")
def read_root():
    return {"message": "MarombAI Backend Operacional 🚀"}

@app.get("/usuarios", response_model=List[User])
def listar_usuarios(session: Session = Depends(get_session)):
    return session.exec(select(User)).all()

@app.get("/treinos")
def listar_treinos(session: Session = Depends(get_session)):
    return session.exec(select(WorkoutPlan)).all()

@app.get("/dietas")
def listar_dietas(session: Session = Depends(get_session)):
    return session.exec(select(DietPlan)).all()

@app.post("/login")
def login(dados: LoginRequest, session: Session = Depends(get_session)):
    statement = select(User).where(User.email == dados.email).where(User.password == dados.password)
    user = session.exec(statement).first()
    
    if not user:
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")
    
    return {
        "status": "sucesso",
        "user_id": user.id,
        "nome": user.nome
    }

@app.get("/user/{user_id}/dashboard")
def get_user_dashboard(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    ultimo_treino = session.exec(select(WorkoutPlan).where(WorkoutPlan.user_id == user_id).order_by(WorkoutPlan.created_at.desc())).first()
    ultima_dieta = session.exec(select(DietPlan).where(DietPlan.user_id == user_id).order_by(DietPlan.created_at.desc())).first()

    return {
        "user": user,
        "treino": json.loads(ultimo_treino.treino_json) if ultimo_treino else None,
        "treino_meta": ultimo_treino,
        "dieta": json.loads(ultima_dieta.dieta_json) if ultima_dieta else None
    }

@app.post("/gerar-treino")
async def gerar_treino(perfil: UserCreate, session: Session = Depends(get_session)):
    # 1. Gerenciar Usuário
    statement = select(User).where(User.email == perfil.email)
    usuario_existente = session.exec(statement).first()

    if usuario_existente:
        usuario_existente.peso = perfil.peso
        usuario_existente.objetivo = perfil.objetivo
        usuario_existente.nivel = perfil.nivel
        usuario_existente.password = perfil.password
        novo_usuario = usuario_existente
        print(f"🔄 Usuário atualizado: {novo_usuario.nome}")
    else:
        novo_usuario = User(
            nome=perfil.nome,
            email=perfil.email,
            password=perfil.password,
            idade=perfil.idade,
            peso=perfil.peso,
            altura=perfil.altura,
            objetivo=perfil.objetivo,
            nivel=perfil.nivel
        )
        session.add(novo_usuario)
        session.commit()
        session.refresh(novo_usuario)
        print(f"✅ Novo usuário criado: {novo_usuario.nome}")

    # 2. Chamar n8n
    # Padrão: localhost (para rodar local). Docker injeta a variável de ambiente para 'n8n'.
    webhook_url = os.getenv("WEBHOOK_URL", "http://localhost:5678/webhook-test/gerar-treino")
    
    payload = {
        "nome": novo_usuario.nome,
        "perfil": perfil.dict()
    }

    print("📡 Enviando para o n8n...")
    
    treino_gerado = None
    dados_n8n = {}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                webhook_url, 
                json=payload, 
                timeout=60.0,
                auth=("admin", "marombai_n8n_secure") 
            )
            
            if response.status_code != 200:
                print(f"❌ Erro n8n: {response.status_code} - {response.text}")
                raise HTTPException(status_code=500, detail=f"Erro n8n: {response.status_code}")
            
            dados_n8n = response.json()
            treino_gerado = dados_n8n.get("treino")
            
            if not treino_gerado and "exercicios" in dados_n8n:
                treino_gerado = dados_n8n
            
            if isinstance(treino_gerado, str):
                cleaned_json = treino_gerado.replace("```json", "").replace("```", "").strip()
                try:
                    treino_gerado = json.loads(cleaned_json)
                except:
                    print(f"⚠️ Falha ao converter string para JSON.")

        except Exception as e:
            print(f"❌ Erro de conexão com n8n: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    # 3. Salvar Treino
    if not treino_gerado:
        raise HTTPException(status_code=502, detail="A IA retornou uma resposta vazia.")

    if treino_gerado and isinstance(treino_gerado, dict):
        exercicios_json_str = json.dumps(treino_gerado.get("exercicios", []))

        novo_plano = WorkoutPlan(
            user_id=novo_usuario.id,
            titulo=treino_gerado.get("titulo", "Treino Personalizado"),
            foco=treino_gerado.get("foco", perfil.objetivo),
            nivel_dificuldade=treino_gerado.get("intensidade", "Média"),
            ai_insight=treino_gerado.get("aiInsight") or treino_gerado.get("ai_insight") or "Análise IA",
            treino_json=exercicios_json_str
        )

        session.add(novo_plano)
        session.commit()
        session.refresh(novo_plano)
        print(f"💾 Treino salvo! ID: {novo_plano.id}")

    return {
        "status": "sucesso",
        "mensagem": "Treino salvo e gerado com sucesso!",
        "user_id": novo_usuario.id,
        "treino_id": novo_plano.id if treino_gerado else None,
        "treino": treino_gerado
    }

@app.post("/gerar-dieta")
async def gerar_dieta(dados: DietRequest, session: Session = Depends(get_session)):
    usuario = session.get(User, dados.user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    webhook_url_dieta = os.getenv("WEBHOOK_URL_DIETA", "http://localhost:5678/webhook-test/gerar-dieta")
    
    user_data = usuario.dict()
    if user_data.get("created_at"):
        user_data["created_at"] = str(user_data["created_at"])

    payload_dieta = {
        "user": user_data,
        "perfil_dieta": dados.dict()
    }

    print("📡 Enviando para o n8n (Dieta)...")
    dieta_gerada = None
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                webhook_url_dieta, 
                json=payload_dieta, 
                timeout=60.0,
                auth=("admin", "marombai_n8n_secure") 
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail=f"Erro n8n: {response.text}")
            
            dados_n8n_dieta = response.json()
            dieta_gerada = dados_n8n_dieta.get("dieta")

            if isinstance(dieta_gerada, str):
                dieta_gerada = json.loads(dieta_gerada.replace("```json", "").replace("```", "").strip())

        except Exception as e:
            print(f"❌ Erro de conexão com n8n (Dieta): {e}")
            raise HTTPException(status_code=500, detail=f"Erro de conexão com a IA: {e}")

    if not dieta_gerada:
        raise HTTPException(status_code=502, detail="A IA de dietas retornou uma resposta inválida.")

    from datetime import datetime
    nova_dieta = DietPlan(
        titulo=f"Dieta para {usuario.nome}",
        objetivo=dados.objetivo,
        restricoes=json.dumps(dados.restricoes),
        dieta_json=json.dumps(dieta_gerada),
        user_id=usuario.id,
        created_at=datetime.utcnow()
    )
    session.add(nova_dieta)
    session.commit()
    session.refresh(nova_dieta)

    return {
        "status": "sucesso",
        "mensagem": "Dieta gerada e salva com sucesso!",
        "dieta_id": nova_dieta.id,
        "dieta": dieta_gerada
    }
