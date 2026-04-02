## Relatório Técnico de Arquitetura: MarombaAI

Este relatório apresenta uma análise crítica da arquitetura atual do projeto MarombaAI e propõe uma nova estrutura baseada em princípios de Clean Architecture para garantir escalabilidade, manutenibilidade e segurança, visando o suporte a 10.000 usuários.

### 1. Resumo da Arquitetura Proposta

A arquitetura atual, embora funcional, apresenta um acoplamento significativo entre as regras de negócio, a lógica de autenticação e a camada de persistência de dados (SQLModel). Para evoluir o sistema, propomos uma transição para uma arquitetura em camadas (Clean Architecture), desacoplando o núcleo do sistema de detalhes de infraestrutura.

**Camadas Propostas:**

1.  **Domínio (Entities):** Contém os objetos de negócio puros (ex: `User`, `Workout`), sem qualquer dependência de frameworks ou banco de dados. São classes Python simples que representam os conceitos centrais do MarombaAI.
2.  **Casos de Uso (Use Cases):** Orquestram o fluxo de dados entre as entidades e as interfaces externas. Contêm a lógica de aplicação (ex: `GerarPlanoDeTreino`, `RegistrarUsuario`). Não conhecem a web (FastAPI) nem o banco de dados (SQLModel).
3.  **Adaptadores de Interface (Interface Adapters):** A "cola" do sistema. Converte dados de formatos externos (HTTP, JSON) para o formato interno do domínio e vice-versa.
    *   **Controllers (FastAPI Endpoints):** Recebem requisições HTTP e invocam os Casos de Uso.
    *   **Repositories:** Implementam interfaces definidas nos Casos de Uso para abstrair o acesso a dados (ex: `UserRepository` que internamente usa SQLModel para buscar um `UserAuth`).
4.  **Infraestrutura (Frameworks & Drivers):** A camada mais externa. Contém FastAPI, SQLModel, Sentry, Loguru, etc. É volátil e pode ser trocada sem impactar o núcleo do sistema.

Este desacoplamento permite que as regras de negócio sejam testadas de forma isolada, facilita a manutenção e permite a troca de componentes de infraestrutura (como o banco dedados ou o framework web) com impacto mínimo.

### 2. Análise de Riscos

#### Segurança (Análise do SRE)

*   **JWT/Bcrypt:** A implementação em `security.py` é sólida, utilizando `bcrypt` para hashing de senhas e JWT para tokens de acesso. A extração da `SECRET_KEY` de variáveis de ambiente é uma boa prática.
    *   **Risco:** O tempo de expiração do token de acesso de 7 dias (`ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7`) é muito longo. Se um token for comprometido, o atacante terá acesso por uma semana.
    *   **Mitigação:** Implementar um sistema de **Refresh Tokens**. Tokens de acesso devem ter vida curta (ex: 15-60 minutos), enquanto um Refresh Token (armazenado de forma segura, possivelmente em um cookie HttpOnly) com vida mais longa (ex: 7 dias) é usado para obter novos tokens de acesso sem exigir que o usuário faça login novamente.
*   **Validação de Credenciais:** A função `get_current_user` valida corretamente a existência do usuário no banco a cada requisição, prevenindo o uso de tokens de usuários que foram deletados.
*   **Escala:** Com 10k usuários, a função `get_current_user` será chamada em quase todas as requisições, adicionando uma consulta ao banco de dados.
    *   **Risco:** Alta carga no banco de dados para validação de tokens.
    *   **Mitigação:** Implementar um cache (ex: Redis) para os dados do usuário associados ao token. A primeira validação busca no banco e armazena em cache com um TTL curto. As próximas requisições com o mesmo token podem validar contra o cache, reduzindo drasticamente os hits no banco.

#### Performance e Concorrência (Análise do SRE e DBA)

*   **Concorrência de Banco de Dados:** O uso de SQLModel com uma sessão por requisição (padrão FastAPI) depende do nível de isolamento de transação do PostgreSQL para gerenciar a concorrência.
    *   **Risco:** Em picos de uso (ex: múltiplos usuários tentando se registrar com o mesmo e-mail ou atualizando o mesmo perfil), podem ocorrer condições de corrida ou deadlocks.
    *   **Mitigação:** Utilizar o gerenciador de pool de conexões do SQLAlchemy (subjacente ao SQLModel) de forma otimizada. Para operações críticas, pode-se implementar um bloqueio otimista (versionamento de linhas) para evitar atualizações conflitantes.
*   **Busca Rápida (Indexação):**
    *   **Análise:** O campo `UserAuth.email` já possui um índice, o que é excelente para a performance de login.
    *   **Risco:** Consultas para buscar o histórico de um usuário (`WorkoutPlan`, `DietPlan`) ou o perfil (`UserProfile`) podem se tornar lentas à medida que as tabelas crescem.
    *   **Mitigação (Estratégia de Indexação):**
        1.  `UserProfile(user_auth_id)`: Essencial. Por ser uma chave estrangeira única, já deve ter um índice, mas é crucial garantir.
        2.  `WorkoutPlan(user_id)`: Adicionar um índice nesta coluna acelerará drasticamente a busca por todos os treinos de um usuário.
        3.  `DietPlan(user_id)`: Mesmo caso do `WorkoutPlan`.
        4.  `WorkoutLog(user_id, workout_plan_id)`: Um índice composto em `(user_id, data_realizacao)` pode otimizar a busca por logs recentes de um usuário.

#### Integridade de Dados (Análise do DBA)

*   **Estrutura das Tabelas:** A separação entre `UserAuth` (autenticação) e `UserProfile` (dados de negócio) é uma excelente decisão de design.
*   **Normalização de Campos JSONB:**
    *   **Risco:** Os campos `lesoes`, `treino_json` e `dieta_json` armazenam estruturas complexas como strings JSON. Isso viola a Primeira Forma Normal (1FN) e traz sérios problemas:
        *   **Impossibilidade de Consultas:** Não é possível fazer consultas eficientes como "Quais usuários têm lesão no joelho?" ou "Qual o exercício mais popular?".
        *   **Integridade de Dados:** Não há como garantir a consistência dos dados dentro do JSON.
        *   **Performance:** O banco de dados trata o campo como um texto opaco, e toda a lógica de parsing ocorre na aplicação.
    *   **Mitigação (Proposta de Normalização):**
        1.  **Lesões:** Criar uma tabela `Lesao` (`id`, `nome`) e uma tabela de associação `UsuarioLesao` (`user_profile_id`, `lesao_id`).
        2.  **Plano de Treino:** Desmembrar `treino_json` em tabelas relacionais:
            *   `Exercicio` (`id`, `nome`, `descricao`, `musculo_alvo`).
            *   `PlanoTreinoExercicio` (`plano_treino_id`, `exercicio_id`, `ordem`, `series`, `repeticoes`, `descanso_segundos`).
        3.  **Plano de Dieta:** Similarmente, desmembrar `dieta_json`:
            *   `Alimento` (`id`, `nome`, `calorias`, `macros_json`).
            *   `Refeicao` (`id`, `plano_dieta_id`, `nome`, `horario`).
            *   `RefeicaoAlimento` (`refeicao_id`, `alimento_id`, `quantidade_gramas`).

### 3. Estratégia de Monitoramento e Observabilidade (Análise do Analista de Monitoramento)

Assumindo que a integração com Sentry e Loguru em `main.py` é básica, a estratégia a seguir visa fornecer visibilidade profunda em um ambiente com 10k usuários.

*   **Métricas Personalizadas (KPIs):** Além das métricas padrão, devemos instrumentar o código para enviar métricas de negócio para uma plataforma como Prometheus ou Datadog.
    *   `marombai_user_registrations_total`: `Counter` - Mede o crescimento da base de usuários.
    *   `marombai_plan_generated_total{type="workout|diet", objective="hipertrofia|emagrecimento"}`: `Counter` com labels - Entender quais funcionalidades são mais usadas.
    *   `marombai_api_request_duration_seconds{endpoint="/path", method="POST"}`: `Histogram` - Identificar gargalos de performance por rota.
    *   `marombai_llm_interaction_errors_total`: `Counter` - Monitorar a saúde da integração com a IA generativa.
*   **Logging Estruturado:**
    *   **Ação:** Configurar o Loguru para emitir logs em **JSON**. Isso permite que sistemas de agregação de logs (ELK, Graylog, Datadog Logs) processem e indexem os logs de forma eficiente.
    *   **Contexto:** Injetar um `request_id` único em cada log gerado durante uma requisição. Isso permite rastrear o fluxo completo de uma operação, desde o recebimento da requisição até a resposta, passando por chamadas a serviços externos.
    *   **Exemplo de Log Estruturado:**
        ```json
        {
          "timestamp": "2023-10-27T10:00:00.123Z",
          "level": "INFO",
          "message": "Workout plan generated successfully",
          "request_id": "x-request-id-12345",
          "user_id": 42,
          "plan_id": 101,
          "generation_time_ms": 1500
        }
        ``````mermaid
graph TD
    subgraph Infraestrutura
        A[FastAPI]
        B[SQLModel]
        C[Sentry/Loguru]
    end

    subgraph Adaptadores de Interface
        D[Controllers/Endpoints]
        E[Repositories (Implementação)]
    end

    subgraph Casos de Uso
        F[GerarPlanoDeTreino]
        G[RegistrarUsuario]
        H[Interfaces de Repositório]
    end

    subgraph Domínio
        I[Entidade User]
        J[Entidade WorkoutPlan]
    end

    A --> D
    D --> F
    D --> G
    F --> H
    G --> H
    E -- Implementa --> H
    E --> B
    F --> I
    F --> J
    G --> I

    style Domínio fill:#f9f,stroke:#333,stroke-width:2px
    style "Casos de Uso" fill:#ccf,stroke:#333,stroke-width:2px
```
*   **Dashboards e Alertas Sugeridos:**
    *   **Dashboard de Saúde da Aplicação:**
        *   Gráficos de Latência (p95, p99) por endpoint.
        *   Taxa de Erros (HTTP 5xx) por endpoint.
        *   Uso de CPU e Memória da aplicação.
        *   **Alerta:** Se a taxa de erro 5xx exceder 1% por 5 minutos.
        *   **Alerta:** Se a latência p99 para o endpoint de geração de treino exceder 3 segundos.
    *   **Dashboard de KPIs de Negócio:**
        *   Novos usuários por dia/semana.
        *   Planos de treino/dieta gerados por dia.
        *   Distribuição de objetivos dos usuários (gráfico de pizza).
        *   **Alerta:** Se o número de registros de novos usuários cair 50% em relação à média da semana anterior.
    *   **Sentry:**
        *   Configurar o `user.id` no escopo do Sentry para associar erros a usuários específicos, facilitando o suporte.
        *   Criar alertas para picos de novos tipos de erro.

### 4. Lista de Melhorias Imediatas (Roadmap para 10k usuários)

1.  **Segurança:** Implementar o fluxo de Refresh Token e diminuir o tempo de vida do Access Token para 15 minutos.
2.  **Banco de Dados:**
    *   Adicionar os índices recomendados nas chaves estrangeiras (`user_id`, `user_auth_id`).
    *   Iniciar a normalização das tabelas, começando pelo `treino_json`, que é central para a aplicação. Criar as tabelas `Exercicio` e `PlanoTreinoExercicio`.
3.  **Arquitetura:** Começar o desacoplamento. Criar a camada de **Domínio** com as entidades `User` e `WorkoutPlan` puras (sem SQLModel) e um **Repository Interface** (`IWorkoutRepository`). Fazer com que o caso de uso `GerarPlanoDeTreino` dependa da interface, não da implementação concreta.
4.  **Observabilidade:** Implementar o logging estruturado com `request_id` e configurar o primeiro dashboard de saúde da aplicação com alertas de latência e taxa de erro.

### 5. Diagrama da Arquitetura Proposta (Mermaid)


**Fluxo de Controle (setas):** A dependência flui sempre para dentro, das camadas externas para as mais internas. A camada de Domínio não conhece nenhuma outra camada. Isso garante que a lógica de negócio, o ativo mais importante do software, seja independente de detalhes de tecnologia.