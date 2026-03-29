# 🛠️ MarombAI - Resumo de Refatoração e Evolução Técnica

Este documento detalha a transição do MarombAI para uma arquitetura de software de classe mundial, focada em segurança, escalabilidade e manutenibilidade.

## 🏗️ 1. Arquitetura Modular (Backend)

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

## 🔐 2. Segurança e Blindagem

Implementamos o padrão **Zero Trust** para proteger os dados dos atletas:

- **Autenticação JWT:** Sessões stateless seguras com tokens assinados digitalmente.
- **Criptografia Bcrypt:** Proteção de senhas no banco de dados (v3.2.0 para compatibilidade).
- **Proteção Anti-IDOR:** Toda rota sensível agora valida a propriedade do recurso (um usuário só acessa/edita o que é dele).
- **Ownership Validation:** Implementação de filtros de "Mass Assignment" para impedir que usuários alterem seus próprios cargos (roles) ou e-mails.
- **Segurança de Reset:** Fluxo de 2 etapas com tokens temporários (60 min) e auditoria completa em tabela dedicada.

## ⚛️ 3. Frontend Moderno (React)

Padronizamos a comunicação e a segurança da interface:

- **Axios Singleton:** Instância centralizada (`api.js`) com interceptores automáticos.
  - Injeção automática de Token JWT no header `Authorization`.
  - Tratamento global de erros 401 (Auto-Logout).
  - Monitoramento de tempo de resposta no console.
- **ProtectedRoute (RBAC):** Componente de alta ordem que gerencia acesso a rotas privadas e valida privilégios de administrador.
- **UX/UI Consistente:** Design System "Cyberpunk Maromba" com feedback visual de progresso, sons sintetizados (Web Audio API) e transições suaves.

## 🌐 4. Infraestrutura e Observabilidade

Preparamos o sistema para rodar em produção com visibilidade total:

- **Logs Estruturados:** Implementação do `Loguru` com rotação diária e persistência em volumes Docker.
- **Performance Tracing:** Middleware para medir o tempo de resposta de cada requisição (`X-Process-Time`).
- **Monitoramento Sentry:** Integração completa no Backend e Frontend para captura de erros e gargalos de performance em tempo real.
- **Caddy Proxy:** Configuração de Proxy Reverso com SSL automático e suporte a subdomínios.

## 🧪 5. Qualidade e Testes

Instituímos uma cultura de código testável:

- **Pytest & Mocks:** Implementação de testes de integração utilizando bancos de dados em memória (SQLite) e Mocks para o serviço de IA (economia de créditos).
- **Code Coverage:** Configuração do `pytest-cov` com barreira de qualidade mínima de 80% de cobertura.
- **Análise Estática:** Configuração do `mypy` para garantir a integridade dos tipos em todo o projeto.
- **CI/CD:** Pipeline do GitHub Actions configurado para rodar testes e linting antes de realizar o deploy automático na VPS.

---

**Nota:** Este documento serve como base para a implementação do `CHANGELOG.md` que seguirá o padrão Semantic Versioning (SemVer).

_Última atualização: 17 de Fevereiro de 2025_
