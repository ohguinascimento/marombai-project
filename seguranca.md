# 🛡️ Relatório de Auditoria de Segurança - MarombAI

**Data:** 17 de Fevereiro de 2025  
**Analista:** Gemini Code Assist  
**Escopo:** Backend (FastAPI), Frontend (React) e Infraestrutura (Docker)

---

## 1. Vulnerabilidades de Severidade CRÍTICA

### 🚨 1.1 Armazenamento de Senhas em Texto Puro
*   **Problema:** Atualmente, o sistema salva a senha do usuário exatamente como ele a digita (`models.py` e `main.py`).
*   **Risco:** Se o banco de dados for comprometido (via SQL Injection ou vazamento de logs), todas as senhas dos usuários estarão expostas imediatamente.
*   **Ajuste Necessário:** Implementar *Hashing* de senhas utilizando bibliotecas como `passlib` com algoritmo `bcrypt` ou `Argon2`. **Nunca** salvar a senha original.

### 🚨 1.2 Ausência de Autenticação Baseada em Token (JWT)
*   **Problema:** O frontend armazena apenas o `user_id` no `localStorage` e o envia nas rotas. O backend não exige um segredo para validar quem está chamando a API.
*   **Risco (IDOR):** Qualquer pessoa pode abrir o navegador, alterar o ID no `localStorage` de `1` para `2` e acessar o dashboard, treinos e dados pessoais de outro usuário.
*   **Ajuste Necessário:** Implementar `OAuth2` com tokens JWT. Cada requisição deve carregar um token assinado pelo servidor.

---

## 2. Vulnerabilidades de Severidade ALTA

### ⚠️ 2.1 Credenciais Expostas no Docker Compose
*   **Problema:** Senhas do banco de dados (`password123`) e do n8n estão escritas diretamente no arquivo `docker-compose.yml`.
*   **Risco:** Se o repositório for privado mas compartilhado, ou se o arquivo for interceptado, o acesso total à infraestrutura é garantido ao atacante.
*   **Ajuste Necessário:** Mover todas as senhas para o arquivo `.env` e referenciá-las no Docker Compose usando variáveis (ex: `${POSTGRES_PASSWORD}`).

### ⚠️ 2.2 Rota de Reset de Senha Sem Verificação
*   **Problema:** A rota `/reset-password` permite que qualquer pessoa altere a senha de qualquer e-mail, bastando saber o endereço.
*   **Risco:** Sequestro de conta em massa.
*   **Ajuste Necessário:** Implementar um fluxo de e-mail com token temporário ou exigir perguntas de segurança/validação multifator.

---

## 3. Vulnerabilidades de Severidade MÉDIA

### 🔍 3.1 Exposição de Detalhes Internos em Erros
*   **Problema:** O backend retorna `str(e)` em blocos `except`.
*   **Risco:** Em caso de erro de banco, o atacante pode receber o nome de colunas, tabelas e até a estrutura de diretórios do servidor.
*   **Ajuste Necessário:** Logar o erro internamente no servidor e retornar apenas mensagens genéricas ao usuário (ex: "Erro interno no servidor").

### 🔍 3.2 Configuração de CORS Permissiva
*   **Problema:** Em desenvolvimento, o `ALLOWED_ORIGINS` aceita `*`.
*   **Risco:** Ataques de *Cross-Site Request Forgery* (CSRF).
*   **Ajuste Necessário:** Em produção, restringir rigorosamente apenas aos domínios `marombai.app` e subdomínios oficiais.

---

## 🚀 Plano de Ação Recomendado

| Ordem | Tarefa | Arquivos Impactados |
| :--- | :--- | :--- |
| 1 | Instalar `passlib[bcrypt]` e criar funções de hash | `backend/main.py`, `backend/models.py` |
| 2 | Implementar JWT para proteger rotas do Dashboard | `backend/main.py`, `frontend/src/pages/Login.jsx` |
| 3 | Sanitizar o `docker-compose.yml` usando segredos do `.env` | `docker-compose.yml`, `.env` |
| 4 | Adicionar validação de e-mail (Regex) e força de senha | `frontend/src/pages/Onboarding.jsx` |

---
**Conclusão:** O MarombAI possui uma arquitetura robusta, mas os mecanismos de proteção de dados são insuficientes para um ambiente público. A prioridade zero deve ser o **Hashing de Senhas** e a **Proteção de Rotas via Token**.
```

### Próximos Passos:
Guilherme, se você desejar, podemos começar agora mesmo a implementar a primeira correção (o **Password Hashing**). É uma alteração rápida que aumenta a segurança do seu banco de dados em 1000%. 

Basta me avisar se quer focar na segurança das senhas ou na proteção das rotas com JWT!

<!--
[PROMPT_SUGGESTION]Como implementar o hashing de senhas com bcrypt no FastAPI?[/PROMPT_SUGGESTION]
[PROMPT_SUGGESTION]Como criar um middleware de autenticação JWT para proteger as rotas do backend?[/PROMPT_SUGGESTION]
->