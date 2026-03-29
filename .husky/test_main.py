from fastapi import status

def test_read_main(client):
    """
    Testa se a rota raiz está online e retornando a mensagem de boas-vindas correta.
    """
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "MarombAI Backend Operacional 🚀"}