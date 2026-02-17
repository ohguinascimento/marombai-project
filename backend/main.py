# --- BIBLIOTECAS EXTERNAS ---
import json
import httpx
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware 
from sqlmodel import Session, select
from contextlib import asynccontextmanager
from typing import List, Optional
from pydantic import BaseModel

# --- ARQUIVOS LOCAIS ---
# O segredo é adicionar o "backend." antes do nome do arquivo
from backend.database import get_session, init_db
from backend.models import User, WorkoutPlan

# --- Modelos de Entrada (Pydantic) ---
# Usados apenas para validar o que chega do Frontend
class UserCreate(BaseModel):
    nome: str
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

# --- Ciclo de Vida ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  # Cria as tabelas se não existirem
    yield

app = FastAPI(lifespan=lifespan)

# --- CONFIGURAÇÃO DO CORS (O porteiro liberando a entrada) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite qualquer origem (Frontend, Postman, etc)
    allow_credentials=True,
    allow_methods=["*"],  # Permite TODOS os métodos (GET, POST, OPTIONS, etc)
    allow_headers=["*"],  # Permite TODOS os headers
)

# --- ROTAS ---

@app.get("/")
def read_root():
    return {"message": "MarombAI Backend Operacional 🚀"}

@app.post("/gerar-treino")
async def gerar_treino(perfil: UserCreate, session: Session = Depends(get_session)):
    """
    1. Recebe dados do Front
    2. Salva/Atualiza Usuário no Banco
    3. Manda para IA (n8n)
    4. Salva o Treino Gerado no Banco
    5. Retorna para o Front
    """
    
    # ---------------------------------------------------------
    # PASSO 1: Gerenciar Usuário (Salvar ou Atualizar)
    # ---------------------------------------------------------
    # Verifica se já existe um usuário com esse nome (simplificação para MVP)
    # No futuro usaremos email ou ID fixo de login
    statement = select(User).where(User.nome == perfil.nome)
    usuario_existente = session.exec(statement).first()

    if usuario_existente:
        # Atualiza os dados se ele mudou de peso ou objetivo
        usuario_existente.peso = perfil.peso
        usuario_existente.objetivo = perfil.objetivo
        usuario_existente.nivel = perfil.nivel
        novo_usuario = usuario_existente
        print(f"🔄 Usuário atualizado: {novo_usuario.nome} (ID: {novo_usuario.id})")
    else:
        # Cria do zero
        novo_usuario = User(
            nome=perfil.nome,
            idade=perfil.idade,
            peso=perfil.peso,
            altura=perfil.altura,
            objetivo=perfil.objetivo,
            nivel=perfil.nivel
        )
        session.add(novo_usuario)
        session.commit()
        session.refresh(novo_usuario)
        print(f"✅ Novo usuário criado: {novo_usuario.nome} (ID: {novo_usuario.id})")

    # ---------------------------------------------------------
    # PASSO 2: Chamar a Inteligência (n8n)
    # ---------------------------------------------------------
    webhook_url = "http://localhost:5678/webhook/gerar-treino" # URL interna do Docker
    
    payload = {
        "nome": novo_usuario.nome,
        "perfil": perfil.dict() # Envia tudo (lesões, local, etc)
    }

    print("📡 Enviando para o n8n...")
    
    async with httpx.AsyncClient() as client:
        try:
            # Adicionando autenticação básica (Usuário, Senha)
                response = await client.post(
                webhook_url, 
                json=payload, 
                timeout=60.0,
                auth=("admin", "marombai_n8n_secure") 
            )
            
                if response.status_code != 200:
                    print(f"❌ Erro n8n: {response.status_code} - {response.text}") # Mostra no terminal
                    raise HTTPException(
                        status_code=500, 
                        detail=f"Erro n8n: {response.status_code} - Verifique se o workflow está ATIVO."
                    )
            
                dados_n8n = response.json()
                treino_gerado = dados_n8n.get("treino") # O JSON puro da IA

        except Exception as e:
            print(f"❌ Erro de conexão com n8n: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    # ---------------------------------------------------------
    # PASSO 3: A Gravadora (Salvar Treino no Banco) 💾
    # ---------------------------------------------------------
    if treino_gerado:
        # Convertendo a lista de exercícios para String JSON para caber no banco
        exercicios_json_str = json.dumps(treino_gerado.get("exercicios", []))

        novo_plano = WorkoutPlan(
            user_id=novo_usuario.id,
            titulo=treino_gerado.get("titulo", "Treino Personalizado"),
            foco=treino_gerado.get("foco", perfil.objetivo),
            nivel_dificuldade=treino_gerado.get("intensidade", "Média"), # Mapeando Intensidade -> Nivel
            ai_insight=treino_gerado.get("aiInsight", "Análise gerada pela IA"),
            treino_json=exercicios_json_str # Salvando o JSON bruto aqui!
        )

        session.add(novo_plano)
        session.commit()
        session.refresh(novo_plano)
        print(f"💾 Treino salvo no banco com sucesso! (ID do Plano: {novo_plano.id})")

    # ---------------------------------------------------------
    # PASSO 4: Retorno ao Frontend
    # ---------------------------------------------------------
    return {
        "status": "sucesso",
        "mensagem": "Treino salvo e gerado com sucesso!",
        "user_id": novo_usuario.id,
        "treino_id": novo_plano.id if treino_gerado else None,
        "treino": treino_gerado # Manda o JSON normal pro React exibir
    }