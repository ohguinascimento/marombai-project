import socket
import os
from sqlalchemy import create_engine, text

def check_port(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    return result == 0

print("--- DIAGNÓSTICO MAROMBAI ---")

# 1. Verificar Banco de Dados
print("\n1. Testando conexão com Banco de Dados (Porta 5432)...")
if check_port(5432):
    print("✅ Porta 5432 está aberta (Docker DB rodando).")
    try:
        # Tenta conectar
        DATABASE_URL = "postgresql://admin:password123@localhost:5432/marombai_db"
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✅ Conexão com PostgreSQL: SUCESSO!")
    except Exception as e:
        print(f"❌ Falha ao logar no banco: {e}")
else:
    print("❌ Porta 5432 fechada. O container do banco (db) não está rodando.")

# 2. Verificar Porta do Backend
print("\n2. Verificando Porta do Backend (8000)...")
if check_port(8000):
    print("⚠️  A porta 8000 JÁ ESTÁ EM USO. Se você não rodou o uvicorn ainda, tem um processo zumbi ou Docker rodando.")
else:
    print("✅ Porta 8000 está livre. Você pode rodar o uvicorn agora.")