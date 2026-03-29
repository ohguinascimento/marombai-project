# 📝 Histórico de Alterações - MarombAI (Fase Alpha)

Este documento detalha as implementações, correções e melhorias realizadas no projeto para garantir a estabilidade da fase Alpha e a preparação para o ambiente de produção.

## 1. Gestão de Usuários e Segurança

- **Normalização de Credenciais:** Implementada a limpeza de strings (`strip()`) e conversão para minúsculas (`lower()`) nos e-mails durante o cadastro e login, eliminando erros de "usuário não encontrado".
- **Redefinição de Senha:** Criada a rota `/reset-password` no backend e interface de recuperação no frontend para permitir a alteração de senhas em caso de erro no cadastro.
- **Confirmação de Senha:** Adicionado campo de validação de senha no Onboarding para prevenir erros de digitação.
- **Sessão e Logoff:**
  - Implementada função de logout limpando o `localStorage`.
  - Criado menu drop-in (dropdown) no avatar do Dashboard para acesso rápido ao Logoff.

## 2. Lógica de Treino (Manual e IA)

- **Seleção Manual de Exercícios:** Adicionado o **Passo 6** no Onboarding, permitindo que o usuário escolha exercícios de uma lista e personalize séries e cargas antes de finalizar.
- **Bypass de IA:** O backend agora detecta se o usuário montou o treino manualmente. Caso positivo, ele pula a integração com n8n/Gemini, garantindo agilidade e economia de recursos.
- **Templates de Treino:** Criada uma biblioteca de treinos pré-cadastrados (Full Body, Push, Pull) que podem ser aplicados diretamente ao perfil do usuário.
- **Fallback de Segurança:** Implementado um "Treino Base" padrão caso a IA esteja offline ou retorne dados inválidos.

## 3. Experiência no Dashboard

- **Modo de Edição (Personalizar):** O botão "Personalizar" no Dashboard agora permite editar séries e cargas dos exercícios do treino atual em tempo real.
- **Persistência de Dados:** Ajustada a busca de dados via API para garantir que o treino e o perfil do usuário sejam carregados corretamente mesmo após a atualização da página (F5).
- **Feedback Visual:** Adicionada tela de carregamento (Loading) customizada com mensagens da IA durante a finalização do perfil.

## 4. Infraestrutura e Banco de Dados

- **Segurança de Variáveis:** Migração de credenciais sensíveis (n8n e Banco de Dados) para variáveis de ambiente utilizando `os.getenv`.
- **Sincronização de Schema:** Atualização dos modelos SQLModel para incluir campos de gênero, frequência, local de treino e dieta, garantindo que o banco de dados reflita todos os dados do formulário.
- **Tratamento de Erros:** Implementação de blocos `try/except` com `session.rollback()` no backend para evitar corrupção de dados e travamentos do servidor.

## 5. Preparação para GitHub e Deploy

- **Arquivo `.gitignore`:** Configurado para ignorar pastas de dependências (`node_modules`, `.venv`), arquivos de ambiente (`.env`) e caches de sistema.
- **Arquivo `.env.example`:** Criado para servir de guia na configuração de novos ambientes de desenvolvimento ou produção.
- **Documentação de Contexto:** Criação do `PROJECT_CONTEXT.md` com a estrutura técnica do projeto (Caddy, Docker, Portas) para suporte e continuidade.

---

_Última atualização: 17 de Fevereiro de 2025_
_Status: Versão Alpha estável para testes online._
