# 🏋️‍♂️ MarombAI - Project Context & Documentation

## 1. Identidade do Projeto
* **Nome:** MarombAI
* **Missão:** Personal Trainer IA que gera treinos personalizados via chat/form.
* **Fase Atual:** Alpha (MVP funcional).
* **Público:** Praticantes de musculação (iniciantes a avançados).

## 2. Infraestrutura (VPS Hostinger)
O projeto roda em containers Docker orquestrados via Docker Compose.

### Estrutura de Serviços
| Serviço | Container Name | Porta Interna | Porta Externa (Host) | Função |
| :--- | :--- | :--- | :--- | :--- |
| **Caddy** | `marombai_caddy` | 80/443 | 80/443 | Proxy Reverso & HTTPS Automático (Gerencia SSL) |
| **Frontend** | `marombai_frontend` | 5173 | 5173 | Interface React + Vite (SPA) |
| **Backend** | `marombai_backend` | 8000 | 8000 | API Python (FastAPI/Flask) |
| **n8n** | `marombai_n8n` | 5678 | 5678 | Automação e Orquestração de IA |
| **Database** | `marombai_db` | 5432 | 5432 | PostgreSQL (Dados de usuários e treinos) |

### Acesso & Caminhos
* **VPS IP:** `148.230.77.18`
* **Usuário:** `root`
* **Caminho do Projeto:** `/root/marombai-project`
* **Edição:** Via VS Code Remote SSH.

### Domínios (DNS)
* `marombai.app` -> Frontend (Atualmente o App Principal, migrando para Landing Page).
* `alpha.marombai.app` -> (Planejado) Será o App de Treino.
* `api.marombai.app` -> Backend API.
* `n8n.marombai.app` -> Editor de Fluxos.

## 3. Visual & UI (Design System)
O visual deve ser mantido estritamente consistente em futuras alterações.

* **Tema:** Dark Mode agressivo ("Cyberpunk Maromba").
* **Paleta de Cores:**
    * **Fundo:** Preto Absoluto (`#000000`) ou Cinza Muito Escuro (`#121212`).
    * **Acento Principal (Primary):** Verde Neon (`#00FF00` ou similar vibrante). Usado em botões de ação, ícones ativos e destaques.
    * **Texto:** Branco (`#FFFFFF`) para títulos, Cinza Claro para descrições.
    * **Cards:** Fundo cinza escuro (`#1E1E1E`) com bordas sutis ou sombras suaves.
* **Tipografia:** Sans-serif moderna, bold em títulos, limpa em leitura.
* **Componentes Chave:**
    * **Botões:** Arredondados, fundo Verde Neon, texto Preto (Alto Contraste).
    * **Input Fields:** Fundo escuro, borda sutil, texto branco.
    * **Barra de Progresso (Onboarding):** Verde Neon sobre fundo cinza.
    * **Dashboard:**
        * Header com saudação "Olá, Maromba".
        * Box "Análise da IA" com destaque visual.
        * Lista de Cards de Exercícios (Nome, Séries, Reps).

## 4. Lógica de IA (O Cérebro)
A inteligência roda no **n8n** conectando ao **Google Gemini 1.5 Pro**.

### Fluxo de Dados
1. **Frontend:** Coleta dados (Nome, Idade, Peso, Altura, Objetivo, Nível).
2. **Backend:** Envia Webhook para n8n.
3. **n8n (Workflow):**
    * Recebe JSON.
    * Monta Prompt para Gemini.
    * **Gemini 1.5 Pro:** Gera JSON estruturado do treino.
    * Parser: Limpa a resposta para JSON válido.
4. **Backend:** Salva no Postgres e devolve ao Frontend.

### Prompt Mestre (Atual)
```text
Você é o MarombAI.
Receba:
Nome: {{ nome }}
Objetivo: {{ objetivo }}
... (outros dados)

TAREFA: Crie um treino JSON.

REGRAS DE OURO:
1. O campo "ai_insight" deve ter MÁXIMO 15 PALAVRAS. Seja direto como um tweet.
2. Retorne APENAS JSON válido.

ESTRUTURA JSON OBRIGATÓRIA:
{
  "titulo": "Nome do Treino",
  "foco": "Grupo Muscular",
  "nivel_dificuldade": "Iniciante/Intermediário/Avançado",
  "ai_insight": "Frase curta e motivadora.",
  "treino": [
    {
      "nome": "Exercício",
      "series": "3",
      "repeticoes": "12",
      "carga": "Moderada",
      "descanso": "60s",
      "dica_execucao": "Dica rápida"
    }
  ]
}