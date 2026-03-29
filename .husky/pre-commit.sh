#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

echo "🧪 [Backend] Rodando testes com Pytest..."

# Tenta executar o pytest usando o python do ambiente virtual
if [ -d "backend/.venv" ]; then
    ./backend/.venv/Scripts/python -m pytest --cov=backend --cov-report=term-missing --cov-report=html:backend/htmlcov backend/
else
    python -m pytest --cov=backend --cov-report=term-missing --cov-report=html:backend/htmlcov backend/
fi

echo "✅ [Backend] Testes passados com sucesso!"

npx lint-staged