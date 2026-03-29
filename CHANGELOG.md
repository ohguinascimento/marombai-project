# 📝 Changelog do MarombAI

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [0.2.0-alpha] - 2025-02-17

### Adicionado

### Alterações de Arquitetura

#### 🏗️ 1. Arquitetura Modular (Backend)

Migramos de um `main.py` monolítico para uma estrutura de **Separação de Responsabilidades (SoC)**:

- **Roteadores (APIRouter):** Divisão por módulos: `auth.py`, `users.py`, `workouts.py`, `generation.py`, `admin.py`.
- **Schemas (Pydantic):** Validação estrita de entrada e saída.
- **Camada de Serviço (`AIService`):** Encapsulamento da lógica IA e tratamento de serialização JSON.

#### 🔐 2. Segurança e Blindagem

- **Zero Trust:** Autenticação JWT e criptografia Bcrypt.
- **Anti-IDOR:** Validação de propriedade de recursos.

#### ⚛️ 3. Frontend Moderno (React)

- **Axios Singleton:** Interceptores para gestão de tokens e erros 401.
- **ProtectedRoute (RBAC):** Controle de acesso administrativo.

#### 🌐 4. Infraestrutura e Observabilidade

- **Sentry & Loguru:** Monitoramento em tempo real e logs estruturados.

## [0.1.0] - 2025-02-10

### Adicionado

- Implementação inicial do sistema de Onboarding e geração de treinos base.
