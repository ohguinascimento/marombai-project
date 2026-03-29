# 🚀 Guia de Deploy: MarombAI na Hostinger (VPS)

Este guia descreve como configurar o ecossistema MarombAI em produção utilizando Docker e Caddy em uma VPS Hostinger (Ubuntu).

## 1. Pré-requisitos de Domínio (DNS)

Antes de mexer no servidor, você precisa apontar seus domínios para o IP da sua VPS (`148.230.77.18`). No seu painel de DNS (Hostinger ou Name.com), crie os seguintes registros do tipo **A**:

| Host/Subdomínio       | Tipo | Valor (IP)    | Função                    |
| :-------------------- | :--- | :------------ | :------------------------ |
| `@` (ou marombai.app) | A    | 148.230.77.18 | Site Principal (Frontend) |
| `api`                 | A    | 148.230.77.18 | API Backend (FastAPI)     |
| `n8n`                 | A    | 148.230.77.18 | Painel de Automação/IA    |

## 2. Preparação da VPS via SSH

Acesse seu servidor e prepare a pasta do projeto:

```bash
ssh root@148.230.77.18
mkdir -p /root/marombai-project
cd /root/marombai-project
```

## 3. Configuração das Variáveis de Ambiente (.env)

Crie o arquivo `.env` na raiz do projeto na VPS. **Não use o mesmo do desenvolvimento local**, pois as URLs agora devem ser HTTPS e usar os domínios reais:

```bash
nano .env
```

**Copie e cole este conteúdo (ajustando as senhas):**

```env
DATABASE_URL=postgresql://admin:SUA_SENHA_FORTE@db:5432/marombai_db
WEBHOOK_URL=https://n8n.marombai.app/webhook/gerar-treino
WEBHOOK_URL_DIETA=https://n8n.marombai.app/webhook/gerar-dieta
N8N_PASSWORD=SUA_SENHA_N8N
N8N_USER=admin
N8N_ENCRYPTION_KEY=uma_chave_aleatoria_longa
```
