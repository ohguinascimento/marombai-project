import pytest
from backend.routers.generation import get_ai_service
from fastapi import status

# 1. Criamos um Mock que simula uma falha na IA (retornando None)
class AIServiceFailureMock:
    async def generate_workout(self, nome: str, perfil: dict):
        return None

    async def generate_diet(self, user_data: dict, diet_profile: dict):
        return None

def test_gerar_treino_deve_retornar_502_quando_ia_falha(client, session):
    """
    Testa se o endpoint /gerar-treino retorna Bad Gateway (502) 
    quando o serviço de IA não consegue gerar o plano.
    """
    # Injetamos o Mock de Falha
    from backend.main import app
    app.dependency_overrides[get_ai_service] = lambda: AIServiceFailureMock()

    payload = {
        "nome": "Atleta Falha",
        "email": "falha_ia@marombai.app",
        "password": "senha_segura",
        "idade": 30,
        "peso": 70,
        "altura": 170,
        "objetivo": "emagrecimento",
        "nivel": "iniciante",
        "frequencia": 3,
        "local": "casa",
        "dieta": "vegano"
    }

    # Chamada para o endpoint
    response = client.post("/gerar-treino", json=payload)

    # Asserts
    assert response.status_code == status.HTTP_502_BAD_GATEWAY
    assert "IA não conseguiu gerar o treino" in response.json()["detail"]

    # Limpa os overrides após o teste
    app.dependency_overrides.clear()
    
    print("\n✅ Teste de erro 502 (IA Offline) validado com sucesso!")