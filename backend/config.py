from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr

class Settings(BaseSettings):
    # Ambiente
    ENV: str = Field("development", description="Ambiente (development ou production)")
    DEBUG: bool = Field(True, description="Modo debug para logs e documentação")

    # Segurança (Obrigatório em produção)
    SECRET_KEY: str = Field(..., description="Chave secreta para JWT")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Integração n8n
    N8N_USER: str = Field(..., min_length=1)
    N8N_PASSWORD: str = Field(..., min_length=1)
    WEBHOOK_URL_TREINO: str = Field(
        "http://n8n:5678/webhook-test/gerar-treino", 
        alias="WEBHOOK_URL"
    )
    WEBHOOK_URL_DIETA: str = "http://n8n:5678/webhook/gerar-dieta"
    
    # CORS - Lista de domínios permitidos
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    # Database
    DATABASE_URL: str = "postgresql://postgres:password123@db:5432/marombai"

    # Configurações do Pydantic para ler o arquivo .env
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()