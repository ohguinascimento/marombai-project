## [0.2.0-alpha] - 2026-03-29
##### Alterações de Arquitetura

Este documento detalha a transição do MarombAI para uma arquitetura de software de classe mundial, focada em segurança, escalabilidade e manutenibilidade.

#### 🏗️ 1. Arquitetura Modular (Backend)

Migramos de um `main.py` monolítico para uma estrutura de **Separação de Responsabilidades (SoC)**:

- **Roteadores (APIRouter):** As rotas foram divididas em módulos lógicos:
  - `auth.py`: Gestão de acesso e recuperação de conta.
  - `users.py`: Perfil do atleta e Dashboard consolidado.
  - `workouts.py`: Gestão de planos, biblioteca de templates e evolução.
  - `generation.py`: Fluxo de Onboarding e orquestração de IA.
  - `admin.py`: Painel de controle global e auditoria de logs.
- **Schemas (Pydantic):** Centralização de todos os modelos de dados em `schemas.py`, garantindo validação estrita de entrada e saída.
- **Camada de Serviço (`AIService`):** Encapsulamento da lógica de integração com n8n e Gemini, incluindo tratamento automático de serialização JSON para objetos `datetime`.
- **Orientação a Objetos (OOP):** Implementação do `SecurityManager` para centralizar a lógica de Hashing e JWT.

#### 🔐 2. Segurança e Blindagem

Implementamos o padrão **Zero Trust** para proteger os dados dos atletas:

- **Autenticação JWT:** Sessões stateless seguras com tokens assinados digitalmente.
- **Criptografia Bcrypt:** Proteção de senhas no banco de dados (v3.2.0 para compatibilidade).
- **Proteção Anti-IDOR:** Toda rota sensível agora valida a propriedade do recurso (um usuário só acessa/edita o que é dele).
- **Ownership Validation:** Implementação de filtros de "Mass Assignment" para impedir que usuários alterem seus próprios cargos (roles) ou e-mails.
- **Segurança de Reset:** Fluxo de 2 etapas com tokens temporários (60 min) e auditoria completa em tabela dedicada.

#### ⚛️ 3. Frontend Moderno (React)

Padronizamos a comunicação e a segurança da interface:

- **Axios Singleton:** Instância centralizada (`api.js`) com interceptores automáticos.
  - Injeção automática de Token JWT no header `Authorization`.
  - Tratamento global de erros 401 (Auto-Logout).
  - Monitoramento de tempo de resposta no console.
- **ProtectedRoute (RBAC):** Componente de alta ordem que gerencia acesso a rotas privadas e valida privilégios de administrador.
- **UX/UI Consistente:** Design System "Cyberpunk Maromba" com feedback visual de progresso, sons sintetizados (Web Audio API) e transições suaves.

#### 🌐 4. Infraestrutura e Observabilidade

Preparamos o sistema para rodar em produção com visibilidade total:

- **Logs Estruturados:** Implementação do `Loguru` com rotação diária e persistência em volumes Docker.
- **Performance Tracing:** Middleware para medir o tempo de resposta de cada requisição (`X-Process-Time`).
- **Monitoramento Sentry:** Integração completa no Backend e Frontend para captura de erros e gargalos de performance em tempo real.
- **Caddy Proxy:** Configuração de Proxy Reverso com SSL automático e suporte a subdomínios.

#### 🧪 5. Qualidade e Testes

Instituímos uma cultura de código testável:

- **Pytest & Mocks:** Implementação de testes de integração utilizando bancos de dados em memória (SQLite) e Mocks para o serviço de IA (economia de créditos).
- **Code Coverage:** Configuração do `pytest-cov` com barreira de qualidade mínima de 80% de cobertura.
- **Análise Estática:** Configuração do `mypy` para garantir a integridade dos tipos em todo o projeto.
- **CI/CD:** Pipeline do GitHub Actions configurado para rodar testes e linting antes de realizar o deploy automático na VPS.

---

**Nota:** Este documento serve como base para a implementação do `CHANGELOG.md` que seguirá o padrão Semantic Versioning (SemVer).

_Última atualização: 17 de Fevereiro de 2025_


# 📝 Changelog do MarombAI

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [0.1.0] - 2026-03-29
### Adicionado

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


## [0.1.0] - 2026-03-29
# 🏋️‍♂️ MarombAI - Resumo Técnico das Implementações

Este documento consolida todas as funcionalidades e melhorias técnicas implementadas no projeto MarombAI durante a fase de desenvolvimento Alpha.

## 🚀 Funcionalidades Core

### 1. Sistema de Onboarding (6 Passos)

- **Identidade:** Coleta de nome, e-mail e senha com normalização automática de strings.
- **Biometria:** Entrada de peso, altura, idade e gênero para cálculos metabólicos.
- **Objetivos:** Definição de foco (Hipertrofia, Emagrecimento, etc.) e nível de experiência.
- **Rotina & Local:** Configuração de frequência semanal e local de treino (Academia, Casa, Ar Livre).
- **Saúde & Dieta:** Mapeamento de lesões, restrições alimentares e suplementação.
- **Customização de Treino:** Seleção manual de exercícios com ajuste de séries e carga antes da geração do plano.

### 2. Engine de Treino & IA

- **Geração Híbrida:** Integração com n8n/Gemini para treinos via IA, com lógica de _bypass_ para treinos montados manualmente pelo usuário.
- **Templates Prontos:** Biblioteca de treinos clássicos (Full Body, Push/Pull) disponíveis para aplicação imediata.
- **Execução Interativa (`WorkoutExecution`):**
  - Cronômetro de sessão em tempo real.
  - Timer de descanso automático baseado no plano.
  - **Feedback Sonoro:** Bipes sintetizados via _Web Audio API_ nos últimos 3 segundos de descanso.
  - **Escala de Esforço (RPE):** Captura da percepção de esforço ao final de cada treino para análise de progressão.

### 3. Dashboard & Acompanhamento

- **Cérebro da IA:** Exibição de _insights_ motivacionais e técnicos gerados pela inteligência artificial.
- **Diário de Treino:** Visualização em _timeline_ de todas as sessões concluídas, incluindo resumo de exercícios e esforço.
- **Página de Evolução:** Estatísticas acumuladas (Total de treinos, tempo dedicado) e gráfico de barras para monitorar a consistência semanal.
- **Personalização de Plano:** Permite editar exercícios, cargas e séries diretamente pelo Dashboard.

## 🛠️ Arquitetura e Backend (FastAPI + SQLModel)

- **Persistência de Dados:** Modelagem completa no PostgreSQL para `User`, `WorkoutPlan`, `WorkoutLog` e `DietPlan`.
- **Segurança de Acesso:**
  - Normalização de e-mails para evitar duplicatas por _case-sensitivity_.
  - Funcionalidade de Reset de Senha e Alteração de Senha com validação da senha antiga.
  - Toggle de visibilidade de senha (ícone de olho) em todos os formulários.
- **Tratamento de Erros:** Implementação de _Rollbacks_ em transações de banco de dados e logs de diagnóstico detalhados no terminal.

## 🎨 UI/UX (Design System)

- **Dark Mode "Cyberpunk Maromba":** Interface baseada em preto absoluto, cinzas profundos e acentos em **Verde Neon**.
- **Responsividade:** Layout focado em dispositivos móveis, simulando uma experiência de aplicativo nativo.
- **Micro-interações:** Animações de transição, estados de _loading_ personalizados e _feedbacks_ visuais de progresso.
- **Central de Configurações:** Página dedicada para gerenciar dados de perfil e preferências do app (como ativar/desativar sons).

## 🤖 Automação & DevOps

- **Relatórios Semanais:** Script Python automático que extrai commits do Git e gera relatórios formatados em Markdown.
- **Integração de Notificações:** Workflow do GitHub Actions que envia os relatórios semanais para **Discord** e **Slack** via Webhooks, com lógica de truncamento para limites de caracteres.
- **Documentação de Infra:** Criação de `PROJECT_CONTEXT.md` e `ALTERACOES.md` para facilitar o _onboarding_ de novos desenvolvedores.
- **Gestão de Ambiente:** Configuração de `.gitignore` e `.env.example` para proteção de credenciais e chaves de API.

---

**Status do Projeto:** Fase Alpha Estável.
**Stack:** React, FastAPI, SQLModel, PostgreSQL, Tailwind CSS, n8n, Gemini AI.


## [0.1.0] - 2025-02-17

### Adicionado

- Implementação de segurança JWT/Bcrypt, rotina de execução de treino e monitoramento Sentry.
