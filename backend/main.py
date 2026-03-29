# --- BIBLIOTECAS EXTERNAS ---
import json
import httpx
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware 
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from contextlib import asynccontextmanager
from typing import List, Optional
from pydantic import BaseModel
import os

# --- ARQUIVOS LOCAIS ---
from backend.database import get_session, init_db
from backend.models import User, WorkoutPlan, DietPlan, WorkoutLog, PasswordResetLog

# --- CONFIGURAÇÃO DE SEGURANÇA (HASHING) ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- CONFIGURAÇÃO JWT ---
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY and os.getenv("ENV") == "production":
    raise RuntimeError("ERRO CRÍTICO: SECRET_KEY não configurada em ambiente de produção!")
SECRET_KEY = SECRET_KEY or "dev_secret_key_only"

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 dias
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

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
    email: str
    new_password: str

class PasswordResetConfirmRequest(BaseModel):
    token: str
    new_password: str

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

# --- Biblioteca de Treinos Pré-cadastrados (Templates) ---
TREINOS_TEMPLATES = [
    {
        "id": 1,
        "titulo": "Adaptação Full Body",
        "foco": "Corpo Inteiro",
        "intensidade": "Iniciante",
        "ai_insight": "Foco em técnica e adaptação neuromuscular para quem está começando.",
        "exercicios": [
            {"nome": "Leg Press 45", "series": "3x15", "carga": "Leve", "descanso": "60s"},
            {"nome": "Puxada Alta", "series": "3x15", "carga": "Leve", "descanso": "60s"},
            {"nome": "Supino Máquina", "series": "3x15", "carga": "Leve", "descanso": "60s"},
            {"nome": "Abdominal Supra", "series": "3x20", "carga": "Peso Corporal", "descanso": "45s"}
        ]
    },
    {
        "id": 2,
        "titulo": "Push (Empurrar) - Hipertrofia",
        "foco": "Peito, Ombro e Tríceps",
        "intensidade": "Intermediário",
        "ai_insight": "Foco em exercícios de empurrar com cadência controlada.",
        "exercicios": [
            {"nome": "Supino Inclinado Halter", "series": "4x10", "carga": "Moderada", "descanso": "90s"},
            {"nome": "Desenvolvimento Militar", "series": "3x10", "carga": "Moderada", "descanso": "90s"},
            {"nome": "Tríceps Testa", "series": "3x12", "carga": "Moderada", "descanso": "60s"},
            {"nome": "Elevação Lateral", "series": "4x15", "carga": "Leve", "descanso": "45s"}
        ]
    },
    {
        "id": 3,
        "titulo": "Pull (Puxar) - Costas e Bíceps",
        "foco": "Costas e Bíceps",
        "intensidade": "Intermediário",
        "ai_insight": "Trabalho focado em tração para densidade das costas.",
        "exercicios": [
            {"nome": "Remada Curvada", "series": "4x10", "carga": "Moderada", "descanso": "90s"},
            {"nome": "Puxada Aberta", "series": "3x12", "carga": "Moderada", "descanso": "60s"},
            {"nome": "Rosca Direta W", "series": "3x10", "carga": "Moderada", "descanso": "60s"},
            {"nome": "Crucifixo Inverso", "series": "3x15", "carga": "Leve", "descanso": "45s"}
        ]
    }
]

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

# --- FUNÇÕES AUXILIARES DE SEGURANÇA ---

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = session.get(User, int(user_id))
    if user is None:
        raise credentials_exception
    return user

def create_password_reset_token(email: str):
    """Gera um token seguro e temporário para reset de senha."""
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode = {"exp": expire, "sub": email, "purpose": "password_reset"}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def send_sendgrid_email(to_email: str, subject: str, html_content: str):
    """Integração real com a API v3 do SendGrid via httpx."""
    api_key = os.getenv("SENDGRID_API_KEY")
    if not api_key:
        print(f"⚠️ SENDGRID_API_KEY ausente. Simulação de e-mail para {to_email}")
        return

    url = "https://api.sendgrid.com/v3/mail/send"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "personalizations": [{"to": [{"email": to_email}]}],
        "from": {"email": "suporte@marombai.app", "name": "MarombAI Support"},
        "subject": subject,
        "content": [{"type": "text/html", "value": html_content}]
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        return response.status_code == 202

async def get_current_admin(current_user: User = Depends(get_current_user)):
    """Verifica se o usuário atual tem privilégios de administrador."""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado: Requer privilégios de administrador"
        )
    return current_user

# --- Ciclo de Vida ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app = FastAPI(
    title="MarombAI API 🏋️‍♂️",
    description="Plataforma de gestão de treinos e dietas baseada em IA.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# --- CONFIGURAÇÃO DO CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ROTAS ---

# --- ROTAS PÚBLICAS/GERAIS ---
@app.get("/", tags=["Geral"])
def read_root():
    return {"message": "MarombAI Backend Operacional 🚀"}

@app.get("/treinos/templates", tags=["Treino"])
def listar_templates():
    """Retorna a biblioteca de treinos pré-definidos."""
    return TREINOS_TEMPLATES

@app.post("/user/{user_id}/selecionar-treino/{template_id}", tags=["Treino"])
def selecionar_treino_template(user_id: int, template_id: int, session: Session = Depends(get_session)):
    """Aplica um treino pré-definido ao perfil do usuário."""
    template = next((t for t in TREINOS_TEMPLATES if t["id"] == template_id), None)
    if not template:
        raise HTTPException(status_code=404, detail="Template de treino não encontrado")
    
    # Criar novo registro de WorkoutPlan para o histórico do usuário
    novo_plano = WorkoutPlan(
        user_id=user_id,
        titulo=template["titulo"],
        foco=template["foco"],
        nivel_dificuldade=template["intensidade"],
        ai_insight=template["ai_insight"],
        treino_json=json.dumps(template["exercicios"])
    )
    
    session.add(novo_plano)
    session.commit()
    session.refresh(novo_plano)
    
    return {"status": "sucesso", "mensagem": "Treino aplicado!", "treino": template}

@app.get("/usuarios", response_model=List[User], dependencies=[Depends(get_current_admin)], tags=["Admin"])
def listar_usuarios(session: Session = Depends(get_session), admin: User = Depends(get_current_admin)):
    return session.exec(select(User)).all()

@app.get("/treinos", dependencies=[Depends(get_current_admin)], tags=["Admin"])
def listar_treinos(session: Session = Depends(get_session)):
    return session.exec(select(WorkoutPlan)).all()

@app.get("/dietas", dependencies=[Depends(get_current_admin)], tags=["Admin"])
def listar_dietas(session: Session = Depends(get_session)):
    return session.exec(select(DietPlan)).all()

@app.get("/admin/security-logs", response_model=List[PasswordResetLog], dependencies=[Depends(get_current_admin)], tags=["Admin"])
def listar_logs_seguranca(session: Session = Depends(get_session)):
    """Retorna todos os logs de segurança ordenados pelos mais recentes."""
    return session.exec(select(PasswordResetLog).order_by(PasswordResetLog.created_at.desc())).all()

@app.post("/login", tags=["Autenticação"])
def login(dados: LoginRequest, session: Session = Depends(get_session)):
    email_normalizado = dados.email.strip().lower()
    print(f"\n🔑 [LOGIN] Tentativa para: {email_normalizado}")
    
    # Primeiro, tentamos achar o usuário apenas pelo email
    user = session.exec(select(User).where(User.email == email_normalizado)).first()
    
    if not user:
        print(f"❌ [LOGIN] Falha: Usuário '{email_normalizado}' não existe no banco.")
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")

    # Se achou o usuário, conferimos a senha
    if not pwd_context.verify(dados.password, user.password):
        print(f"❌ [LOGIN] Falha: Senha incorreta para '{email_normalizado}'.")
        print(f"   Tentativa com senha inválida para o hash no banco.")
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")

    print(f"✅ [LOGIN] Sucesso: {user.nome} (ID: {user.id})")
    
    # Gera o Token JWT
    access_token = create_access_token(data={"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {"id": user.id, "nome": user.nome, "role": user.role}
    }

@app.post("/reset-password", tags=["Autenticação"])
async def request_password_reset(dados: PasswordResetRequest, request: Request, session: Session = Depends(get_session)):
    """Inicia o fluxo de reset enviando o e-mail com token."""
    email_normalizado = dados.email.strip().lower()
    
    # Captura metadados para o log
    ip = request.client.host
    ua = request.headers.get("user-agent")

    user = session.exec(select(User).where(User.email == email_normalizado)).first()
    
    if not user:
        # Registra tentativa falha (usuário inexistente)
        log = PasswordResetLog(email=email_normalizado, action="request", status="user_not_found", ip_address=ip, user_agent=ua)
        session.add(log)
        session.commit()
        
        # Por segurança, não informamos se o e-mail existe ou não
        return {"status": "sucesso", "mensagem": "Se o e-mail existir, um link de recuperação foi enviado."}
    
    token = create_password_reset_token(email_normalizado)
    reset_link = f"https://marombai.app/reset-password/confirm?token={token}"
    
    html = f"<p>Olá {user.nome},</p><p>Clique no link abaixo para resetar sua senha:</p><a href='{reset_link}'>{reset_link}</a>"
    await send_sendgrid_email(email_normalizado, "Recuperação de Senha - MarombAI", html)
    
    # Registra sucesso na solicitação
    log = PasswordResetLog(email=email_normalizado, action="request", status="success", ip_address=ip, user_agent=ua)
    session.add(log)
    session.commit()

    return {"status": "sucesso", "mensagem": "E-mail de recuperação enviado."}

@app.post("/reset-password/confirm", tags=["Autenticação"])
def confirm_password_reset(dados: PasswordResetConfirmRequest, request: Request, session: Session = Depends(get_session)):
    """Valida o token e define a nova senha."""
    ip = request.client.host
    ua = request.headers.get("user-agent")
    email_log = "unknown"

    try:
        payload = jwt.decode(dados.token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("purpose") != "password_reset":
            raise HTTPException(status_code=400, detail="Token inválido para esta operação")
        email = payload.get("sub")
        email_log = email
    except JWTError:
        log = PasswordResetLog(email=email_log, action="confirm", status="failed", ip_address=ip, user_agent=ua)
        session.add(log)
        session.commit()
        raise HTTPException(status_code=400, detail="Token expirado ou inválido")

    user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        log = PasswordResetLog(email=email_log, action="confirm", status="user_not_found", ip_address=ip, user_agent=ua)
        session.add(log)
        session.commit()
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    user.password = pwd_context.hash(dados.new_password)
    
    log = PasswordResetLog(email=email_log, action="confirm", status="success", ip_address=ip, user_agent=ua)
    session.add(log)
    
    session.add(user)
    session.commit()
    return {"status": "sucesso", "mensagem": "Senha atualizada com sucesso!"}

@app.put("/user/{user_id}/password", tags=["Usuário"])
def atualizar_senha(user_id: int, dados: ChangePasswordRequest, session: Session = Depends(get_session)):
    """Altera a senha do usuário validando a senha atual."""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Validação de segurança: a senha antiga deve estar correta
    if not pwd_context.verify(dados.old_password, user.password):
        raise HTTPException(status_code=400, detail="Senha atual incorreta")
    
    user.password = pwd_context.hash(dados.new_password)
    session.add(user)
    session.commit()
    
    return {"status": "sucesso", "mensagem": "Senha alterada com sucesso!"}

@app.put("/user/{user_id}", tags=["Usuário"])
def atualizar_perfil(user_id: int, dados: UserUpdate, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    """Atualiza dados básicos do perfil do usuário sem alterar o treino."""
    # Proteção contra IDOR: Usuário só pode editar a si mesmo
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Você não tem permissão para editar este perfil")

    user = current_user
    update_data = dados.dict(exclude_unset=True)
    
    # Proteção contra Mass Assignment: Impede alteração de campos sensíveis
    campos_bloqueados = ["id", "email", "role", "created_at"]
    for key, value in update_data.items():
        if key not in campos_bloqueados:
            setattr(user, key, value)
    
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return {"status": "sucesso", "usuario": user}

@app.put("/workout/{workout_id}", tags=["Treino"])
def atualizar_treino(workout_id: int, dados: WorkoutUpdate, session: Session = Depends(get_session)):
    """Atualiza um plano de treino existente."""
    workout = session.get(WorkoutPlan, workout_id)
    if not workout:
        raise HTTPException(status_code=404, detail="Treino não encontrado")
    
    if dados.titulo:
        workout.titulo = dados.titulo
    if dados.foco:
        workout.foco = dados.foco
    if dados.nivel_dificuldade:
        workout.nivel_dificuldade = dados.nivel_dificuldade
    if dados.ai_insight:
        workout.ai_insight = dados.ai_insight
    
    workout.treino_json = json.dumps(dados.exercicios)
    
    session.add(workout)
    session.commit()
    session.refresh(workout)
    return {"status": "sucesso", "treino": json.loads(workout.treino_json), "meta": workout}

@app.post("/workout/finish", tags=["Treino"])
def finalizar_treino(dados: WorkoutLogCreate, session: Session = Depends(get_session)):
    """Registra a conclusão de uma sessão de treino."""
    try:
        novo_log = WorkoutLog(
            user_id=int(dados.user_id),
            workout_plan_id=int(dados.workout_plan_id),
            duracao_minutos=dados.duracao_minutos,
            esforco_percebido=int(dados.esforco_percebido),
            detalhes_json=json.dumps(dados.detalhes_exercicios)
        )
        session.add(novo_log)
        session.commit()
        return {"status": "sucesso", "log_id": novo_log.id}
    except Exception as e:
        session.rollback()
        print(f"❌ Erro ao salvar log de treino: {e}")
        raise HTTPException(status_code=500, detail="Erro ao salvar histórico de treino.")

@app.get("/user/{user_id}/evolution", tags=["Usuário"])
def get_user_evolution(user_id: int, session: Session = Depends(get_session)):
    """Busca o histórico de treinos para mostrar a evolução."""
    statement = select(WorkoutLog).where(WorkoutLog.user_id == user_id).order_by(WorkoutLog.data_realizacao.asc())
    logs = session.exec(statement).all()

    return [
        {
            "id": log.id,
            "data": log.data_realizacao.strftime("%d/%m"),
            "duracao": log.duracao_minutos,
            "esforco": log.esforco_percebido,
            "observacoes": log.observacoes,
            "exercicios": json.loads(log.detalhes_json) if log.detalhes_json else []
        } for log in logs
    ]

# --- ROTA PROTEGIDA EXEMPLO ---

@app.get("/user/dashboard/me", tags=["Dashboard"])
def get_user_dashboard(
    current_user: User = Depends(get_current_user), 
    session: Session = Depends(get_session)
):
    user = current_user
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    user_id = user.id
    ultimo_treino = session.exec(select(WorkoutPlan).where(WorkoutPlan.user_id == user_id).order_by(WorkoutPlan.created_at.desc())).first()
    ultima_dieta = session.exec(select(DietPlan).where(DietPlan.user_id == user_id).order_by(DietPlan.created_at.desc())).first()

    return {
        "user": user,
        "treino": {
            "titulo": ultimo_treino.titulo,
            "foco": ultimo_treino.foco,
            "intensidade": ultimo_treino.nivel_dificuldade,
            "ai_insight": ultimo_treino.ai_insight,
            "exercicios": json.loads(ultimo_treino.treino_json)
        } if ultimo_treino else None,
        "treino_meta": ultimo_treino,
        "dieta": json.loads(ultima_dieta.dieta_json) if ultima_dieta else None
    }

@app.post("/gerar-treino", tags=["Geração IA"])
async def gerar_treino(perfil: UserCreate, session: Session = Depends(get_session)):
    # 1. Gerenciar Usuário
    email_normalizado = perfil.email.strip().lower()
    statement = select(User).where(User.email == email_normalizado)
    usuario_existente = session.exec(statement).first()

    if usuario_existente:
        usuario_existente.peso = perfil.peso
        usuario_existente.objetivo = perfil.objetivo
        usuario_existente.nivel = perfil.nivel
        usuario_existente.frequencia = perfil.frequencia
        usuario_existente.local = perfil.local
        usuario_existente.dieta = perfil.dieta
        usuario_existente.lesoes = json.dumps(perfil.lesoes)
        usuario_existente.password = pwd_context.hash(perfil.password)
        novo_usuario = usuario_existente
        try:
            session.add(novo_usuario)
            session.commit()
            session.refresh(novo_usuario)
            print(f"🔄 Usuário atualizado: {novo_usuario.nome}")
        except Exception as e:
            session.rollback()
            print(f"❌ Erro ao atualizar usuário: {e}")
            raise HTTPException(status_code=500, detail="Erro ao atualizar dados no banco.")
    else:
        novo_usuario = User(
            nome=perfil.nome,
            email=email_normalizado,
            password=pwd_context.hash(perfil.password),
            idade=perfil.idade,
            peso=perfil.peso,
            altura=perfil.altura,
            objetivo=perfil.objetivo,
            nivel=perfil.nivel,
            genero=perfil.genero,
            frequencia=perfil.frequencia,
            local=perfil.local,
            dieta=perfil.dieta,
            lesoes=json.dumps(perfil.lesoes)
        )
        try:
            session.add(novo_usuario)
            session.commit()
            session.refresh(novo_usuario)
            print(f"✅ Novo usuário criado com ID {novo_usuario.id}: {novo_usuario.nome}")
        except Exception as e:
            session.rollback()
            print(f"❌ Erro fatal ao criar usuário: {e}")
            raise HTTPException(status_code=500, detail=f"Erro ao salvar no banco: {str(e)}")

    # 2. Chamar n8n
    treino_gerado = None

    # Se o usuário enviou exercícios manuais, usamos eles e pulamos a IA
    if perfil.exercicios and len(perfil.exercicios) > 0:
        print("🛠️ Usando exercícios selecionados manualmente.")
        treino_gerado = {
            "titulo": f"Treino de {novo_usuario.nome}",
            "foco": perfil.objetivo,
            "intensidade": "Personalizada",
            "ai_insight": "Treino montado manualmente. Foco total na execução!",
            "exercicios": perfil.exercicios
        }
    else:
        # LOGICA IA (Comentada/Desativada por enquanto conforme solicitado)
        # webhook_url = os.getenv("WEBHOOK_URL", "http://localhost:5678/webhook-test/gerar-treino")
        # payload = {"nome": novo_usuario.nome, "perfil": perfil.dict()}
        # print("📡 Enviando para o n8n...")
        # async with httpx.AsyncClient() as client:
        #     try:
        #         response = await client.post(webhook_url, json=payload, timeout=60.0, auth=("admin", "marombai_n8n_secure"))
        #         if response.status_code == 200:
        #             dados_n8n = response.json()
        #             treino_gerado = dados_n8n.get("treino")
        #             if not treino_gerado and "exercicios" in dados_n8n: treino_gerado = dados_n8n
        #             if isinstance(treino_gerado, str):
        #                 treino_gerado = json.loads(treino_gerado.replace("```json", "").replace("```", "").strip())
        #     except Exception as e:
        #         print(f"❌ Erro IA: {e}")
        
        # Fallback caso a IA esteja desativada e não venha exercícios manuais
        if not treino_gerado:
             treino_gerado = {
                "titulo": "Treino Base",
                "foco": "Adaptação",
                "intensidade": "Leve",
                "ai_insight": "Inicie com cargas leves para aprender a técnica.",
                "exercicios": [
                    {"nome": "Agachamento Livre", "series": "3x12", "carga": "Leve", "descanso": "60s"},
                    {"nome": "Supino Reto", "series": "3x12", "carga": "Leve", "descanso": "60s"},
                    {"nome": "Remada Curvada", "series": "3x12", "carga": "Leve", "descanso": "60s"}
                ]
            }

    # 3. Salvar Treino
    if not treino_gerado:
        raise HTTPException(status_code=502, detail="A IA retornou uma resposta vazia.")

    novo_plano = None
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
        "treino_id": novo_plano.id if novo_plano else None,
        "treino": treino_gerado
    }

@app.post("/gerar-dieta", tags=["Geração IA"])
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
                auth=(
                    os.getenv("N8N_USER", "admin"), 
                    os.getenv("N8N_PASSWORD", "marombai_n8n_secure")
                ) 
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
