# backend/Dockerfile

# 1. Imagem Python atualizada
FROM python:3.12-slim

# 2. Configurações
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Define a pasta raiz de trabalho no container
WORKDIR /app

# 4. Instala dependências do sistema
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# 5. Copia e instala requirements (fica na raiz /app)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. --- A CORREÇÃO MÁGICA ---
# Em vez de jogar os arquivos soltos, copiamos para dentro de uma pasta 'backend'
# Assim o container fica igual ao seu Windows: /app/backend/main.py
COPY . ./backend

# 7. Comando para rodar
# Como estamos na pasta /app, o Python consegue achar "backend.main"
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]