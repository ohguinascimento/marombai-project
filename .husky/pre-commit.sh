#!/usr/bin/env sh

# echo "🧪 [MarombAI] Validando lógica e cobertura do Backend..."

# Adiciona o diretório atual ao PYTHONPATH para que o Python encontre o pacote 'backend'
# export PYTHONPATH=$PYTHONPATH:.

# if [ -f "backend/.venv/Scripts/python" ]; then
#     ./backend/.venv/Scripts/python -m pytest -c backend/pyproject.toml --cov=backend --cov-report=term-missing
# else
#     python -m pytest -c backend/pyproject.toml --cov=backend --cov-report=term-missing
# fi

# if [ $? -ne 0 ]; then
#     echo "❌ [MarombAI] A cobertura mínima (80%) não foi atingida ou os testes falharam."
#     exit 1
# fi

npx lint-staged