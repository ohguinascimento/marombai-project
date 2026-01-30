# MarombAI 🏋️‍♂️🤖

> Assistente Inteligente para Gestão de Treinos, Dieta e Saúde.

Este projeto é uma API desenvolvida para auxiliar no acompanhamento de métricas de saúde, utilizando Inteligência Artificial para otimizar rotinas de treino e alimentação.

---

## 🛠 Tech Stack

* **Linguagem:** Python 3.12
* **Framework:** FastAPI
* **Banco de Dados:** PostgreSQL (via Docker)
* **ORM:** SQLAlchemy
* **Infraestrutura:** Docker & Docker Compose
* **Automação:** n8n (Integrado no Docker)

---

## 🚀 Como Rodar o Projeto

### 1. Pré-requisitos
Certifique-se de ter instalado:
* [Git](https://git-scm.com/)
* [Docker Desktop](https://www.docker.com/)
* [Python 3.12](https://www.python.org/)

### 2. Clonar o Repositório

```bash
git clone [https://github.com/duartebruno496/marombai-project.git](https://github.com/duartebruno496/marombai-project.git)
cd marombai-project

3. Configurar Infraestrutura (Docker)

Suba o banco de dados e os serviços auxiliares:
Bash

docker-compose up -d

    Nota: O PostgreSQL rodará na porta 5432. Certifique-se de não ter outro serviço ocupando esta porta.

4. Configurar o Backend

Entre na pasta do backend:
Bash

cd backend

Crie um arquivo .env baseado nas configurações locais. Exemplo:
Ini, TOML

# Arquivo: backend/.env
DATABASE_URL=postgresql://admin:password123@127.0.0.1:5432/marombai_db

Crie o ambiente virtual e instale as dependências:
Bash

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente (Windows)
.\venv\Scripts\activate

# Instalar pacotes
pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic python-dotenv

5. Executar a API

Com o ambiente virtual ativo, inicie o servidor:
Bash

python -m uvicorn main:app --reload

Estrutura do Projeto
marombai-project/
├── backend/            # API Python (FastAPI)
│   ├── main.py         # Entrada da aplicação
│   ├── database.py     # Conexão com Banco
│   ├── models.py       # Tabelas do Banco (SQLAlchemy)
│   └── venv/           # Ambiente Virtual (Ignorado no Git)
├── docker-compose.yml  # Orquestração de Containers
└── README.md           # Documentação

Status do Projeto

