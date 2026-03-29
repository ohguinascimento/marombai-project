# 🔐 MarombAI - Documentação de Implementações de Segurança

Este documento detalha as camadas de segurança implementadas no ecossistema MarombAI para proteger os dados dos usuários e garantir o acesso autorizado.

## 1. Proteção de Credenciais (Password Hashing)
- **Algoritmo:** Utilização do `bcrypt` via biblioteca `passlib`.
- **Implementação:** 
    - As senhas nunca são armazenadas em texto puro.
    - No cadastro e alteração de senha, o sistema gera um hash único utilizando o método `pwd_context.hash()`.
    - Durante o login, a validação é feita através do método `pwd_context.verify()`, que compara a senha digitada com o hash armazenado de forma segura.
- **Arquivos Relacionados:** `backend/main.py`, `backend/models.py`.

## 2. Autenticação Baseada em Token (JWT)
- **Padrão:** JSON Web Tokens (JWT) utilizando a biblioteca `python-jose`.
- **Fluxo de Login:** 
    - Após a verificação das credenciais, o servidor emite um token assinado com uma `SECRET_KEY`.
    - O token contém a identidade do usuário (`sub: user_id`) e uma data de expiração.
- **Proteção de Rotas:** 
    - Implementação da dependência `get_current_user` no FastAPI.
    - O backend extrai o ID do usuário diretamente do token assinado, prevenindo ataques de **IDOR** (Insecure Direct Object Reference), onde um usuário tentaria acessar dados de outro alterando o ID na URL.
- **Arquivos Relacionados:** `backend/main.py`.

## 3. Controle de Acesso Baseado em Papéis (RBAC)
- **Hierarquia:** Implementação de níveis de acesso: `user` e `admin`.
- **Validação de Admin:** 
    - Criada a dependência `get_current_admin` que valida se o papel (`role`) gravado no token possui privilégios administrativos.
    - Rotas sensíveis como `/usuarios`, `/treinos` e `/dietas` (listagem global) são restritas exclusivamente a administradores.
- **Arquivos Relacionados:** `backend/main.py`, `backend/models.py`.

## 4. Segurança no Frontend (React)
- **Interceptores Axios:** 
    - Implementação de uma instância centralizada do Axios (`api.js`).
    - **Request Interceptor:** Anexa automaticamente o token JWT no cabeçalho `Authorization: Bearer <token>` em todas as requisições.
    - **Response Interceptor:** Detecta automaticamente erros `401 Unauthorized` (token expirado ou inválido), limpa o armazenamento local e redireciona o usuário para o Login.
- **ProtectedRoute:** Componente de alta ordem que encapsula rotas privadas, verificando a existência do token e o nível de acesso (`allowedRoles`) antes de renderizar a página.
- **Sanitização de Dados:** Normalização automática de e-mails (`lowercase` e `trim`) para evitar duplicidade e erros de login.
- **Arquivos Relacionados:** `frontend/src/api/api.js`, `frontend/src/components/ProtectedRoute.jsx`.

## 5. Infraestrutura e Redes
- **Configuração de CORS:** Restrição de acesso à API via variável de ambiente `ALLOWED_ORIGINS`, permitindo apenas domínios autorizados (`marombai.app` e subdomínios).
- **Segurança de Variáveis:** Uso de arquivos `.env` e `.gitignore` para garantir que chaves de API (Gemini, n8n) e segredos de banco de dados não sejam expostos no controle de versão.
- **Proxy Reverso (Caddy):** O Caddy atua como única porta de entrada (80/443), gerenciando SSL automático e protegendo os containers internos (`backend`, `db`, `n8n`) de exposição direta à internet.

---
**Observação:** Todas as implementações seguem as recomendações da auditoria de segurança realizada em 17/02/2025.
```

Este relatório cobre todos os pontos que transformaram o MarombAI em uma aplicação com padrões profissionais de segurança. Com o JWT e o RBAC configurados, você tem total controle sobre quem acessa o quê.

<!--
[PROMPT_SUGGESTION]Como configurar o GitHub Actions para validar se não há segredos expostos no código antes do push?[/PROMPT_SUGGESTION]
[PROMPT_SUGGESTION]Como implementar uma política de expiração de token mais curta com Refresh Tokens para maior segurança?[/PROMPT_SUGGESTION]
->