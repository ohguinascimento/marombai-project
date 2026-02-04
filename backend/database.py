from sqlmodel import SQLModel, create_engine, Session

# String de Conexão (Conversando com o Docker)
# usuario:senha@localhost:porta/nome_do_banco
# Atualize com as credenciais novas que você colocou no Docker
DATABASE_URL = "postgresql://admin:password123@127.0.0.1:5432/marombai_db"

# O motor que faz a conexão real
engine = create_engine(DATABASE_URL, echo=True) # echo=True mostra o SQL no terminal (bom para debug)

# Função para criar as tabelas no banco
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Dependência para pegar a sessão do banco (usada nas rotas)
def get_session():
    with Session(engine) as session:
        yield session