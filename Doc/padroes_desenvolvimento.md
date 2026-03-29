# 🛠️ Padrões de Desenvolvimento - MarombAI

Este documento define as diretrizes técnicas para manter a consistência, segurança e qualidade do ecossistema MarombAI.

## 1. Princípios Gerais

- **KISS (Keep It Simple, Stupid):** Evite complexidade desnecessária. Se a lógica estiver difícil de explicar, ela precisa ser refatorada.
- **DRY (Don't Repeat Yourself):** Lógicas repetidas devem ser extraídas para funções utilitárias ou serviços.
- **Clean Code:** Nomes de variáveis devem ser descritivos (ex: `user_weight_kg` em vez de `uw`).

## 2. Backend (FastAPI + SQLModel)

- **Camada de Serviço:** O roteador (`router`) lida apenas com requisições. A lógica de negócio reside em `services/`.
- **Schemas (Pydantic):** Nunca retorne ou receba modelos do banco de dados diretamente. Use Schemas para validação e serialização.
- **Tipagem:** O uso de *Type Hints* é obrigatório em todas as funções.
- **Logs:** Utilize o `loguru` para rastreamento. Nunca use `print()`.

## 3. Frontend (React + Vite)

- **Componentização:** Componentes com mais de 200 linhas devem ser divididos.
- **Estilização:** Utilize exclusivamente **Tailwind CSS**. Mantenha a paleta "Cyberpunk" (Dark Bg + Neon Green).
- **API:** Todas as chamadas devem usar a instância centralizada do Axios em `api/api.js`.

## 4. Git e Versionamento

- **Conventional Commits:** Siga rigorosamente o padrão `tipo(escopo): descrição`.
    - `feat`: Nova funcionalidade.
    - `fix`: Correção de erro.
    - `sec`: Melhoria de segurança.
    - `docs`: Documentação.
- **Hooks:** Nunca force um push que falhe no Husky (Pytest ou Security Score).

## 5. Segurança

- **Secrets:** Nunca armazene chaves ou senhas no código. Use o `config.py` e `.env`.
- **PII:** Nunca registre dados sensíveis de usuários (senhas, tokens) nos logs.

---
**Última Atualização:** 18/02/2025