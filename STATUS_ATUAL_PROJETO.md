# 🏋️‍♂️ MarombAI - Status Atual do Projeto (Fase Alpha Pro)

Este documento resume o progresso técnico e as funcionalidades implementadas no MarombAI, refletindo uma arquitetura robusta, segura e escalável.

## 🚀 Funcionalidades de Negócio (Core)

### 1. Inteligência de Treino & Execução
- **Geração de Treinos:** Sistema híbrido que suporta montagem manual de treinos ou geração via IA (n8n + Gemini).
- **Execução Ativa (`WorkoutExecution`):** Interface focada com cronômetro de sessão, timer de descanso automático e dicas de execução.
- **Feedback Sensorial:** Integração com a *Web Audio API* para bipes sonoros nos últimos 3 segundos de descanso.
- **Monitoramento de Carga:** Escala RPE (Percepção Subjetiva de Esforço) integrada à finalização do treino.

### 2. Acompanhamento e Evolução
- **Diário de Treino:** Linha do tempo (timeline) cronológica de todas as sessões finalizadas com resumo de exercícios.
- **Dashboard de Evolução:** Gráficos de barras dinâmicos construídos com Tailwind CSS para visualização de volume semanal e consistência.
- **IA de Dieta:** Endpoint integrado para geração de planos alimentares personalizados baseados no perfil biométrico.

## 🛡️ Segurança e Proteção de Dados (The Shield)

### Autenticação de Elite
- **Criptografia:** Implementação de `bcrypt` (v3.2.0) para hashing de senhas, garantindo que credenciais nunca sejam salvas em texto puro.
- **Tokens JWT:** Sistema de autenticação *stateless* com JSON Web Tokens assinados digitalmente.
- **RBAC (Controle de Acesso):** Hierarquia de usuários (`user` e `admin`) protegendo rotas sensíveis no backend e frontend.

### Blindagem de API
- **Proteção Anti-IDOR:** Validação de propriedade de recursos (um usuário não pode acessar treinos ou evolução de outro).
- **Interceptadores Axios:** Injeção automática de tokens e tratamento global de erros 401 (Auto-Logout).
- **Auditoria:** Registro detalhado de logs de reset de senha, capturando IP e metadados do navegador.

## 🏗️ Arquitetura e Engenharia

### Backend (FastAPI + SQLModel)
- **Tratamento Global de Erros:** Middleware para capturar exceções de banco de dados e evitar vazamento de informações técnicas para o usuário.
- **Performance:** Middleware para medição de tempo de resposta (`X-Process-Time`) em cada requisição.
- **Logs Estruturados:** Implementação do `Loguru` com rotação diária de arquivos e persistência em volumes Docker.

### Frontend (React + Vite)
- **ProtectedRoute:** Componente de Alta Ordem (HOC) para blindagem de rotas privadas.
- **Single Instance API:** Centralização de chamadas via Axios, facilitando a troca de ambientes (Dev vs Prod).
- **UX Cyberpunk:** Design system baseado em cores neon sobre fundo dark, focado em performance mobile.

## 🌐 Infraestrutura e Observabilidade

### DevOps & Deploy
- **Docker Compose:** Orquestração completa de 5 serviços (Frontend, Backend, Postgres, n8n, Caddy).
- **Proxy Reverso (Caddy):** Gerenciamento automático de certificados SSL (HTTPS) e roteamento de subdomínios.
- **CI/CD:** Workflow do GitHub Actions configurado para deploy automático na Hostinger via SSH.

### Monitoramento Proativo
- **Sentry Integration:** Monitoramento de erros e performance tanto no Backend (FastAPI) quanto no Frontend (React).
- **Tracing Distribuído:** Capacidade de rastrear o tempo de processamento desde o clique do usuário até a resposta da IA.

## 📋 Próximos Passos (Roadmap)

1.  **Gamificação:** Implementação de sistema de XP e Níveis baseados na consistência do Diário.
2.  **Progressão IA:** Algoritmo para sugerir aumento de cargas baseado no histórico de RPE.
3.  **App Mobile Nativo:** Utilização da base de API atual para criação de app via Flutter ou React Native.

---
**Data da última revisão:** 17 de Fevereiro de 2025  
**Engenheiro Responsável:** Guilherme (Atleta/Dev) & Gemini Code Assist
```

Este arquivo agora é o seu consolidado oficial. Ele demonstra que o projeto atingiu um nível de maturidade técnica muito alto para uma fase Alpha, especialmente nos quesitos de segurança e infraestrutura.

O que você gostaria de ajustar agora? Podemos focar em refinar os gráficos de evolução ou talvez iniciar a lógica de gamificação (XP/Níveis)?

<!--
[PROMPT_SUGGESTION]Como implementar o sistema de XP e Níveis baseado nos minutos de treino salvos no Diário?[/PROMPT_SUGGESTION]
[PROMPT_SUGGESTION]Como configurar um Dashboard Administrativo para ver as métricas de performance do Sentry?[/PROMPT_SUGGESTION]
->