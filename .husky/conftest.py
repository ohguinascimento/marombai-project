import pytest
from fastapi.testclient import TestClient
from backend.main import app

@pytest.fixture(scope="module")
def client():
    """
    Cria uma instância do TestClient que será compartilhada entre os testes.
    O bloco 'with' garante que o lifespan (init_db) seja executado.
    """
    with TestClient(app) as c:
        yield c