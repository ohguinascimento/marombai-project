# MAROMBAI - Documentação Técnica e Contexto (RAG)

## 1. Visão Geral
O MarombAI é uma aplicação web que gera treinos de musculação hiper-personalizados utilizando Inteligência Artificial. O sistema coleta dados biomecânicos do usuário, processa via LLM e devolve um plano estruturado.

## 2. Stack Tecnológica
- **Frontend:** React (Vite), TailwindCSS, Lucide React.
- **Backend:** Python (FastAPI), SQLModel (SQLAlchemy), Pydantic.
- **Banco de Dados:** PostgreSQL (Dockerizado).
- **Orquestração/IA:** n8n (Dockerizado) integrado com Google Gemini.
- **Infraestrutura:** Docker Compose gerenciando serviços (App, DB, n8n).

## 3. Estrutura de Pastas Importantes
/marombai-project
├── /backend
│   ├── main.py       # API Gateway, Rotas e Lógica de Orquestração
│   ├── models.py     # Esquemas do Banco de Dados (SQLModel)
│   ├── database.py   # Conexão com Postgres
│   └── __init__.py   # Define o pacote
├── /frontend
│   ├── src/pages     # Telas (Onboarding, Dashboard)
│   └── src/components # Componentes reutilizáveis
├── docker-compose.yml # Definição dos containers (DB e n8n)
└── CONTEXT.md        # Este arquivo

## 4. Banco de Dados (Schema)

### Tabela: User
- `id`: int (PK)
- `nome`: str
- `idade`: int
- `peso`: float
- `altura`: int
- `objetivo`: str (ex: "hipertrofia", "emagrecimento")
- `nivel`: str (ex: "iniciante", "avançado")
- `created_at`: datetime

### Tabela: WorkoutPlan
- `id`: int (PK)
- `user_id`: int (FK -> User.id)
- `titulo`: str (Nome criativo do treino)
- `foco`: str (ex: "Upper Body", "Full Body")
- `nivel_dificuldade`: str
- `ai_insight`: str (Explicação científica do treino)
- `treino_json`: str (TEXT/JSON) -> Contém a lista completa de exercícios, séries e repetições.
- `created_at`: datetime

## 5. Fluxo de Dados (Pipeline de Geração)
1. **Frontend:** Coleta dados no form (Onboarding) e envia POST para `/gerar-treino`.
2. **Backend (FastAPI):**
   - Recebe payload.
   - Verifica se usuário existe (pelo nome) -> Cria ou Atualiza no Postgres (`User`).
   - Envia payload para Webhook do n8n (`http://localhost:5678/webhook/gerar-treino`).
3. **n8n (IA):**
   - Recebe JSON.
   - Monta prompt para o Google Gemini.
   - Retorna JSON estruturado (Título, Foco, Array de Exercícios).
4. **Backend:**
   - Recebe resposta da IA.
   - Salva registro na tabela `WorkoutPlan` (convertendo array de exercícios para string JSON).
   - Retorna dados completos para o Frontend.

## 6. Comandos de Execução
- **Ativar Ambiente Virtual:** `.\.venv\Scripts\Activate`
- **Backend:** `python -m uvicorn backend.main:app --reload`
- **Frontend:** `npm run dev` (na pasta frontend)
- **Docker:** `docker-compose up -d`

## 7. Status Atual (Alpha)
- Sistema funcional rodando localmente.
- Persistência de dados completa.
- Integração n8n autenticada e ativa.