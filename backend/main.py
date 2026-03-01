# --- Modelos de Entrada para Dieta ---
class DietRequest(BaseModel):
    user_id: int
    objetivo: str
    restricoes: list = []
    preferencias: list = []
    dieta: str = "onivoro"
    suplementos: list = []

# --- Endpoint para gerar dieta personalizada ---
@app.post("/gerar-dieta")
async def gerar_dieta(dados: DietRequest, session: Session = Depends(get_session)):
    """
    1. Recebe dados do Front
    2. Busca usuário
    3. Gera dieta personalizada (mock/IA)
    4. Salva dieta no banco
    5. Retorna dieta
    """
    # 1. Buscar usuário
    usuario = session.get(User, dados.user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # 2. Mock de geração de dieta (substituir por IA/n8n depois)
    dieta_gerada = {
        "refeicoes": [
            {"nome": "Café da manhã", "itens": ["Ovos mexidos", "Aveia", "Banana"]},
            {"nome": "Almoço", "itens": ["Arroz integral", "Frango grelhado", "Salada"]},
            {"nome": "Jantar", "itens": ["Peixe", "Batata doce", "Brócolis"]}
        ],
        "objetivo": dados.objetivo,
        "restricoes": dados.restricoes,
        "preferencias": dados.preferencias,
        "dieta": dados.dieta,
        "suplementos": dados.suplementos
    }

    # 3. Salvar dieta no banco
    from datetime import datetime
    import json
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
# O segredo é adicionar o "backend." antes do nome do arquivo
from backend.database import get_session, init_db
from backend.models import User, WorkoutPlan, DietPlan

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

@app.get("/usuarios", response_model=List[User])
def listar_usuarios(session: Session = Depends(get_session)):
    """
    Retorna a lista de todos os usuários cadastrados.
    """
    users = session.exec(select(User)).all()
    return users

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
    #webhook_url = "http://localhost:5678/webhook/gerar-treino" # URL interna do Docker (antiga para teste local)
    webhook_url = os.getenv("WEBHOOK_URL", "http://localhost:5678/webhook/gerar-treino")
    
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
                # Tenta pegar a chave 'treino', se não existir, assume que o JSON inteiro é o treino
                treino_gerado = dados_n8n.get("treino")
                
                if not treino_gerado and "exercicios" in dados_n8n:
                    print("⚠️ Aviso: JSON veio sem a chave raiz 'treino', usando o corpo inteiro.")
                    treino_gerado = dados_n8n

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