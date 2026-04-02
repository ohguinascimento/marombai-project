# --- BIBLIOTECAS EXTERNAS ---
import sentry_sdk
import os
import time
import uuid
from loguru import logger
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware 
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from contextlib import asynccontextmanager
from sentry_sdk.integrations.fastapi import FastApiIntegration

# --- ARQUIVOS LOCAIS ---
from backend.database import init_db
from backend.routers import auth
from backend.config import settings
from backend.routers import workouts
from backend.routers import users
from backend.routers import admin
from backend.routers import generation

# --- CONFIGURAÇÃO SENTRY ---
SENTRY_DSN = os.getenv("SENTRY_DSN")
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[FastApiIntegration()],
        traces_sample_rate=float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", 1.0)),
        profiles_sample_rate=float(os.getenv("SENTRY_PROFILES_SAMPLE_RATE", 1.0)),
        environment=os.getenv("ENV", "development"),
        send_default_pii=True
    )
    logger.info("📡 Sentry inicializado com sucesso!")

# --- Ciclo de Vida ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="MarombAI API 🏋️‍♂️",
    description="Plataforma de gestão de treinos e dietas baseada em IA.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    openapi_url="/openapi.json" if settings.DEBUG else None
)

# Limpa espaços extras e converte a string do config em lista
origins = [origin.strip() for origin in settings.ALLOWED_ORIGINS.split(",")]

# --- CONFIGURAÇÃO DO CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Process-Time", "X-Request-ID"], # Permite que o frontend leia estes headers
)

# --- MIDDLEWARE DE PERFORMANCE ---
@app.middleware("http")
async def monitorar_tempo_resposta(request: Request, call_next):
    # Gera um ID único para rastreabilidade (Correlation ID)
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    
    # Adiciona headers de observabilidade
    response.headers["X-Process-Time"] = str(round(process_time, 4))
    response.headers["X-Request-ID"] = request_id
    
    logger.info(f"⏱️ {request.method} {request.url.path} | ID: {request_id} | Tempo: {process_time:.4f}s")
    return response

# --- TRATAMENTO GLOBAL DE EXCEÇÕES ---

@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """Captura erros genéricos de banco de dados e impede vazamento de logs no JSON."""
    # Logamos o erro real no terminal/arquivo para o desenvolvedor
    logger.error(f"[DATABASE ERROR] no endpoint {request.url.path}: {str(exc)}")
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Ocorreu um erro interno ao processar os dados no servidor."}
    )

@app.exception_handler(IntegrityError)
async def integrity_exception_handler(request: Request, exc: IntegrityError):
    """Captura erros de integridade, como e-mails duplicados."""
    logger.warning(f"[INTEGRITY ERROR] no endpoint {request.url.path}: {str(exc)}")
    
    # Verifica se é erro de e-mail duplicado (comum no cadastro)
    detail = "Conflito de integridade nos dados enviados."
    if "userauth.email" in str(exc).lower():
        detail = "Este e-mail já está cadastrado no sistema."

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": detail}
    )

# --- IMPORTAÇÃO DOS ROTEADORES ---
app.include_router(auth.router, prefix="/auth", tags=["Autenticação"])
app.include_router(workouts.router, prefix="/workout", tags=["Treino"])
app.include_router(users.router, prefix="/user", tags=["Usuário"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(generation.router, tags=["IA"])

@app.get("/", tags=["Geral"])
def read_root():
    return {"message": "MarombAI Backend Operacional 🚀"}
