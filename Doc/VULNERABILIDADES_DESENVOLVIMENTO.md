# 🛠️ Auditoria de Vulnerabilidades de Desenvolvimento - MarombAI

**Data:** 17 de Fevereiro de 2025  
**Status:** Pendente de Correção

---

## 1. Vulnerabilidades Lógicas (Nível Crítico)

### 🚨 1.1 Bypass Total no Reset de Senha
*   **Vulnerabilidade:** A rota `/reset-password` aceita um e-mail e uma nova senha sem qualquer validação de identidade (token de e-mail, pergunta de segurança ou senha antiga).
*   **Risco:** Um atacante pode trocar a senha de qualquer usuário (incluindo admins) apenas sabendo o e-mail dele.
*   **Correção:** Desativar a rota em produção até a implementação de um serviço de e-mail (SendGrid/Mailgun) com tokens temporários.

### 🚨 1.2 Chave Secreta Exposta e Padrão
*   **Vulnerabilidade:** O `SECRET_KEY` possui um valor padrão no código.
*   **Risco:** Se o desenvolvedor esquecer de configurar a variável de ambiente na Hostinger, o sistema usará a chave padrão, permitindo que atacantes forjem tokens JWT válidos.
*   **Correção:** Forçar o encerramento do servidor se a chave não for fornecida via `.env`.

---

## 2. Vulnerabilidades de Dados (Nível Alto)

### ⚠️ 2.1 Mass Assignment no Update de Perfil
*   **Vulnerabilidade:** A função `atualizar_perfil` usa `setattr(user, key, value)` diretamente do dicionário enviado pelo usuário.
*   **Risco:** Um usuário mal-intencionado pode enviar `"role": "admin"` no corpo do JSON de atualização de perfil e se auto-promover a administrador.
*   **Correção:** Filtrar rigorosamente quais campos podem ser editados na rota de perfil.

### ⚠️ 2.2 Falta de Validação de Formato (Campos de Entrada)
*   **Vulnerabilidade:** O sistema aceita qualquer string como e-mail ou nome.
*   **Risco:** Injeção de scripts (XSS) ou poluição do banco de dados com dados inválidos.
*   **Correção:** Usar validações nativas do Pydantic (`EmailStr`, `min_length`, `max_length`).

---

## 3. Infraestrutura (Nível Médio)

### 🔍 3.1 Falta de Rate Limiting
*   **Vulnerabilidade:** Não há limite de tentativas de login ou chamadas à API.
*   **Risco:** Ataques de força bruta (Brute Force) contra senhas e sobrecarga do n8n/Gemini por bots.
*   **Correção:** Implementar `slowapi` ou configurar limite de requisições no Caddy.

---
*Nota: Este relatório foca em erros introduzidos durante a aceleração das funcionalidades Alpha.*