from sqlmodel import SQLModel, create_engine, Session

# --- Configuração da Conexão ---

# A estrutura é: postgresql://USUARIO:SENHA@HOST:PORTA/NOME_DO_BANCO
DATABASE_URL = "postgresql://admin:password123@localhost:5432/marombai_db"

# Cria a engine de conexão
engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    """Cria as tabelas no banco se elas não existirem"""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Dependência para criar uma sessão de banco por requisição"""
    with Session(engine) as session:
        yield session