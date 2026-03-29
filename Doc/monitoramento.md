# 🚀 Notas de Lançamento (Release Notes)

## 🔐 Segurança e Autenticação (Zero Trust)

- **Password Hashing:** Migração completa de senhas em texto puro para hashes irreversíveis utilizando `bcrypt` (v3.2.0).
- **Autenticação JWT:** Implementação de tokens de acesso assinados digitalmente, eliminando a dependência de IDs expostos e protegendo contra ataques de **IDOR**.
- **RBAC (Controle de Acesso):** Estruturação de hierarquia entre `user` e `admin`, com blindagem de rotas sensíveis tanto no Backend quanto no Frontend via `ProtectedRoute`.
- **Auditoria de Segurança:** Implementação de logs detalhados para tentativas de reset de senha, capturando metadados como IP e User Agent.

## 🏋️‍♂️ Engine de Treino e Evolução

- **Módulo de Execução:** Nova interface interativa com cronômetro de sessão, timer de descanso automatizado e feedback sonoro via **Web Audio API**.
- **Logs de Performance:** Persistência real de treinos finalizados com escala **RPE** (Percepção de Esforço).
- **Visualização de Dados:** Implementação do **Diário** (timeline cronológica) e **Evolução** (gráficos de barras dinâmicos via Tailwind).

## 🏗️ Engenharia de Software e Robustez

- **Arquitetura de API:** Centralização de chamadas via instância **Axios** com _Interceptors_ para injeção automática de tokens e tratamento global de erros 401 (Auto-Logout).
- **Resiliência:** Implementação de _Global Exception Handlers_ para capturar falhas de banco de dados e evitar vazamento de informações técnicas sensíveis.
- **Observabilidade:** Integração do **Sentry** (Back e Front) para monitoramento de erros e performance em tempo real.
- **Logs Estruturados:** Migração para o **Loguru** com persistência em volume Docker e rotação diária de arquivos.

## 🌐 Infraestrutura e DevOps

- **Docker Pro:** Otimização dos containers e volumes para persistência de dados e logs.
- **Ambientes Dinâmicos:** Separação clara de configurações entre Desenvolvimento e Produção (Hostinger).

---

_Gerado automaticamente para documentação de ciclo de vida do projeto MarombAI._
