from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models
from database import engine, get_db

# Comando mágico que cria as tabelas no banco automaticamente
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="MarombAI API")

@app.get("/")
def read_root():
    return {"message": "MarombAI API rodando com sucesso!"}

@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    # Rota simples para testar se o banco responde
    users = db.query(models.User).all()
    return users