# Fluxo de Autenticação - MarombAI

Este documento descreve o funcionamento técnico da autenticação e autorização no projeto MarombAI, abrangendo os componentes Backend (FastAPI) e Frontend (React).

## 1. Tecnologias Utilizadas

- **Backend:** FastAPI, SQLModel (ORM), Jose (JWT), Passlib (Hashing de senha).
- **Frontend:** React, Axios (Interceptors), LocalStorage.

## 2. Fluxo de Registro (Onboarding)

O registro ocorre ao final do formulário de Onboarding:

1. O Frontend envia os dados do usuário para `POST /auth/register`.
2. O Backend recebe a senha em texto puro e aplica um **Hash** utilizando `SecurityManager.hash_password` antes de salvar no banco de dados.
3. Após o salvamento, o Backend gera um **JWT (JSON Web Token)**.
4. A resposta retorna o `access_token` e os dados básicos do usuário.
5. O Frontend armazena o token no `localStorage` sob a chave `marombai_token`.

## 3. Fluxo de Login

1. O usuário fornece e-mail e senha.
2. O Backend busca o usuário pelo e-mail e utiliza `SecurityManager.verify_password` para comparar a senha fornecida com o hash armazenado.
3. Se válido, um novo JWT é emitido.

## 4. Gestão de Tokens no Frontend (Axios Interceptors)

A comunicação segura é gerenciada centralizadamente no arquivo `src/api/api.js`:

### Interceptor de Requisição

Antes de qualquer chamada à API, o sistema verifica se existe um token no `localStorage`. Caso exista, ele é injetado automaticamente no cabeçalho:
`Authorization: Bearer <token>`

### Interceptor de Resposta

O sistema monitora as respostas do servidor. Se o Backend retornar um erro **401 Unauthorized** (token expirado ou inválido):

1. O `localStorage` é limpo.
2. O usuário é redirecionado automaticamente para a página de `/login`.

## 5. Proteção de Rotas no Backend

As rotas que exigem identificação do usuário (como `/workout/cadastrar-treino`) utilizam a dependência `get_current_user`.

```python
@router.post("/cadastrar-treino")
def cadastrar(current_user: User = Depends(get_current_user)):
    # O FastAPI valida o JWT no header antes de executar esta função
```

## 6. Recuperação de Senha

1. **Solicitação:** `POST /auth/reset-password` gera um token temporário com `purpose: password_reset` e envia via e-mail (ou log de simulação).
2. **Confirmação:** `POST /auth/reset-password/confirm` valida a assinatura do token e a expiração antes de permitir a alteração da senha no banco de dados.

---

**Observação de Segurança:**

- As senhas nunca são armazenadas em texto puro.
- O Secret Key e Algoritmo (HS256) são definidos via variáveis de ambiente.
- O tempo de expiração do token é controlado pelo Backend.
