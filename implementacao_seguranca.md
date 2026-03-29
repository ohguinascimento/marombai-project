# 🛠️ Detalhamento de Implementação - MarombAI

Este documento fornece uma visão profunda da arquitetura de software e das decisões de engenharia tomadas durante o desenvolvimento da fase Alpha do MarombAI.

## 1. Arquitetura do Sistema

O sistema segue o padrão de **Arquitetura de Microserviços Descentralizados**, orquestrados via Docker Compose:

- **Frontend (React + Vite):** Uma Single Page Application (SPA) de alta performance.
- **Backend (FastAPI):** Um servidor assíncrono baseado em Python que prioriza velocidade e tipagem estática com Pydantic.
- **Database (PostgreSQL):** Banco de dados relacional para garantir a integridade referencial entre usuários, planos e logs.
- **Automação (n8n):** Camada de orquestração low-code para integração flexível com modelos de linguagem (LLMs) como o Gemini.
- **Proxy Reverso (Caddy):** Camada de infraestrutura que gerencia o tráfego externo e provê criptografia TLS (HTTPS) automática.

## 2. Implementações de Segurança (World-Class Standards)

### Autenticação e Autorização
- **Password Hashing:** Utilizamos `passlib` com o algoritmo `bcrypt`. Ao contrário da criptografia simétrica, o hashing é um processo de via única, garantindo que mesmo com acesso ao banco de dados, as senhas reais não possam ser revertidas.
- **JWT (JSON Web Tokens):** Implementamos tokens assinados digitalmente. Isso permite que o backend seja *stateless* (sem estado), escalando horizontalmente com facilidade, pois a validação do usuário reside na assinatura do token e não em sessões de memória no servidor.
- **Role-Based Access Control (RBAC):** Estruturamos uma hierarquia de acesso (`user` vs `admin`) tanto no nível de API (via dependências do FastAPI) quanto no nível de interface (via `ProtectedRoute` no React).

### Blindagem de Rotas (Anti-IDOR)
 Em vez de rotas como `/user/1/dashboard`, implementamos a rota `/user/dashboard/me`. O ID do usuário nunca é confiado via parâmetro de URL, mas sim extraído do *payload* decodificado do token JWT enviado no header `Authorization`.

## 3. Core Engine de Treino

### Fluxo de Execução e RPE
- **Módulo `WorkoutExecution`:** Implementamos um gerenciador de estado que controla a sessão ativa de treino.
- **Web Audio API:** Para os bipes de descanso, optamos por sintetizar o som via código em vez de carregar arquivos MP3. Isso reduz o consumo de banda e elimina a latência de carregamento.
- **Captura de Esforço (RPE):** O sistema utiliza a escala de Percepção Subjetiva de Esforço. Esse dado é fundamental para futuras implementações de *Progressive Overload* (Progressão de Carga) automatizada por IA.

### Persistência de Histórico (Logs)
 Criamos a tabela `WorkoutLog` que salva instantâneos (snapshots) do treino realizado. Mesmo que o plano de treino mude no futuro, o registro histórico do que foi feito naquele dia específico permanece íntegro.

## 4. Estrutura do Frontend (React Patterns)

### Axios Interceptors (Padrão Singleton)
 Centralizamos todas as chamadas de API em uma instância única (`api.js`). 
 **Auto-Token:** O interceptor injeta o token JWT em cada requisição de saída.
 **Auto-Logout:** O interceptor de resposta detecta erros 401 (token expirado) e limpa o `localStorage` globalmente, forçando o redirecionamento para o login sem que o desenvolvedor precise tratar isso em cada página.

### Roteamento Declarativo
 Utilizamos o `react-router-dom` com o componente de alta ordem `ProtectedRoute`. Isso garante que o código das páginas privadas nem sequer seja montado se o critério de autenticação ou papel (role) não for atendido.

## 5. Engenharia de Dados e Evolução

### Visualização Cyberpunk
 O gráfico de evolução diária foi construído puramente com Tailwind CSS, utilizando cálculos de escala dinâmica baseados no valor máximo do conjunto de dados (`Math.max(...chartData)`). Isso garante que o gráfico seja responsivo e visualmente equilibrado independentemente do volume de treinos.

### Normalização de Dados
 Implementamos rotinas de limpeza (`strip`, `lower`) na entrada de e-mails para garantir consistência no banco de dados e evitar duplicidade de contas por erros de digitação.

## 6. Infraestrutura e DevOps

### Deployment Pipeline (CI/CD)
 Configuramos GitHub Actions com o `appleboy/ssh-action`. O fluxo automatizado realiza o `git pull` e o `docker-compose build` diretamente na VPS, garantindo que o ambiente de produção seja um espelho exato da branch `main`.

### HTTPS Automático com Caddy
 Escolhemos o Caddy pela sua integração nativa com o Let's Encrypt. Ele remove a complexidade de renovação manual de certificados e gerencia o roteamento de subdomínios (`api`, `n8n`) de forma declarativa.

## 7. Próximos Passos Técnicos

1. **Refresh Tokens:** Para permitir sessões mais longas sem comprometer a segurança dos Access Tokens.
2. **WebSockets:** Para feedbacks em tempo real durante a execução do treino caso tenhamos múltiplos dispositivos.
3. **Sentry/Logging:** Implementação de monitoramento de erros em tempo real no backend.

---
**Engenheiro Responsável:** Gemini Code Assist  
**Data da Documentação:** 17/02/2025
```

Este documento é excelente para ser lido por qualquer desenvolvedor que entrar no projeto, pois ele explica a inteligência por trás dos arquivos. Ele mostra que o MarombAI não é apenas um conjunto de telas, mas um sistema pensado para ser **seguro, escalável e fácil de manter**.

<!--
[PROMPT_SUGGESTION]Como documentar as rotas da API automaticamente usando o Swagger UI nativo do FastAPI?[/PROMPT_SUGGESTION]
[PROMPT_SUGGESTION]Como configurar o Sentry no backend para monitorar erros de produção automaticamente?[/PROMPT_SUGGESTION]
->