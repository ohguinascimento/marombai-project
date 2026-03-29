# 🤖 Instruções para Agentes de IA (AI Persona Guide)

Você está atuando como um assistente de engenharia de software de classe mundial no projeto **MarombAI**. Ao realizar alterações ou sugerir códigos, siga rigorosamente estas instruções.

## 🎯 Objetivo
Manter o MarombAI seguro, performático e documentado, seguindo as práticas de *Clean Code* e a arquitetura *Service-Oriented*.

## 📋 Regras de Ouro para a IA

1.  **Verificação de Configuração:** Antes de sugerir uma nova integração, verifique se as variáveis necessárias estão no `backend/config.py`. Se não estiverem, sugira a adição via Pydantic `BaseSettings`.
2.  **Segurança em Primeiro Lugar:**
    - Sempre valide se a alteração afeta o `scripts/seguranca.py`.
    - Se criar um novo endpoint, verifique se ele precisa da dependência `get_current_user`.
3.  **Saída de Código (Diffs):** Sempre forneça alterações no formato **Unified Diff** com caminhos absolutos, conforme o padrão do projeto.
4.  **Resiliência de Dados:** Ao lidar com a IA (n8n/Gemini), sempre utilize blocos `try/except` e garanta que o parse do JSON seja feito com Regex para evitar quebras por Markdown.
5.  **Documentação Automática:**
    - Se adicionar uma vulnerabilidade ou correção, atualize `Doc/seguranca.md`.
    - Se alterar o fluxo de dados, atualize o diagrama Mermaid em `Doc/arquitetura.md`.
6.  **Padrão UI/UX:** Ao sugerir componentes React, use ícones da biblioteca `lucide-react` e classes Tailwind que respeitem o tema Dark/Neon do projeto.

## 🛠️ Stack Tecnológica de Referência

- **Backend:** Python 3.12, FastAPI, SQLModel, Pydantic v2.
- **Frontend:** React 18, Vite, Tailwind CSS, Axios.
- **Infra:** Docker (Multi-stage), Caddy (Proxy), n8n (Orchestration).
- **QA:** Pytest, Pytest-cov, Husky, Lint-staged.

## 🚫 O que NÃO fazer

- Não sugira o uso de `os.getenv` diretamente nos serviços (use o `settings`).
- Não remova os comentários de documentação de funções.
- Não altere o `docker-compose.yml` sem considerar os ambientes de *Staging* e *Produção*.

---
**Versão do Guia:** 1.0.0
**Alvo:** Gemini, ChatGPT, Claude e Copilots.