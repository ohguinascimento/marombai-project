# 🚀 Atualizações Recentes - MarombAI (Fase Alpha Pro)

Este documento resume as implementações de segurança, infraestrutura e funcionalidades core realizadas na última sprint de desenvolvimento.

## 🔐 Segurança e Autenticação (Zero Trust)
- **Criptografia de Senhas (Hashing):** Implementação do `bcrypt` (v3.2.0) via `passlib`. As senhas agora são protegidas por hashes irreversíveis no banco de dados, eliminando o armazenamento em texto puro.
- **Autenticação JWT (JSON Web Tokens):** Transição para tokens assinados digitalmente. O servidor agora emite tokens de acesso com expiração, garantindo que a identidade do usuário seja validada em cada requisição.
- **Proteção Anti-IDOR:** Refatoração de rotas sensíveis para utilizarem o contexto do token (`/user/dashboard/me`). O sistema identifica o usuário pela assinatura do token e não apenas por IDs numéricos na URL.
- **RBAC (Role-Based Access Control):** Implementação de níveis de acesso (`user` e `admin`). Rotas administrativas e logs de segurança agora são restritos exclusivamente a perfis autorizados.
- **Auditoria de Segurança:** Criação da tabela `PasswordResetLog` para monitorar tentativas de recuperação de conta, capturando IP e User Agent para detecção de anomalias.

## 🏋️‍♂️ Experiência de Treino e Evolução
- **Módulo de Execução Interativa:** Nova interface de treino com cronômetro de sessão e timer de descanso automatizado.
- **Feedback Sonoro (Web Audio API):** Implementação de bipes sintetizados nos segundos finais do descanso, funcionando sem dependência de arquivos externos.
- **Escala RPE (Percepção de Esforço):** Sistema de avaliação pós-treino para monitorar a intensidade real e permitir ajustes futuros via IA.
- **Visualização de Dados:** 
    - **Diário:** Visual em timeline cronológica de todas as sessões realizadas.
    - **Evolução:** Gráficos de barras dinâmicos (Tailwind) para análise de volume e consistência semanal.

## 🛠️ Arquitetura e Engenharia de Frontend
- **Padronização com Axios:** Criação de uma instância centralizada da API (`api.js`) com interceptores automáticos.
    - **Auto-Auth:** O token JWT é anexado automaticamente em todas as chamadas.
    - **Auto-Logout:** Redirecionamento instantâneo para o login em caso de token expirado (Erro 401).
- **ProtectedRoute (HOC):** Componente de alta ordem que protege rotas privadas e valida privilégios de administrador antes da renderização.
- **UX de Acesso:** Implementação de visibilidade de senha (ícone de olho) e confirmação de segurança no cadastro.

## 🤖 Recuperação de Conta (Password Reset)
- **Fluxo de Token Seguro:** Sistema de reset via e-mail utilizando tokens JWT de curta duração (15 min) com propósito específico.
- **Integração SendGrid:** Backend preparado para envio de e-mails transacionais via API.
- **Página de Confirmação:** Interface dedicada para validação do token e definição de nova credencial.

## 🌐 Infraestrutura e DevOps
- **Ambientes Dinâmicos:** Configuração de arquivos `.env.development` e `.env.production` para alternância automática de endpoints entre Localhost e Hostinger.
- **Docker Pro:** Reestruturação dos containers para ocultar portas internas e utilizar o **Caddy** como único ponto de entrada seguro (HTTPS).
- **CI/CD:** Workflow do GitHub Actions configurado para deploy automático na VPS via SSH ao realizar push na branch `main`.
- **Auditoria de Logs:** Nova dashboard administrativa para visualização, filtragem por IP/E-mail e exportação de logs de segurança para CSV.

---
**Status Atual:** Sistema Estável e Blindado.  
**Próximo Foco:** Refinamento dos prompts da IA e expansão da base de exercícios.

_Atualizado em: 17 de Fevereiro de 2025_
