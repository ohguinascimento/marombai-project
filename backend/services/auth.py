from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from services.auth_service import AuthService

# Define onde o FastAPI deve procurar o token (no header Authorization: Bearer ...)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Dependência para validar o token JWT e retornar a identidade do usuário.
    Lança 401 Unauthorized se o token for inválido ou expirado.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Putz! Sua sessão expirou ou o token é inválido. Faz login de novo?",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = AuthService.decode_token(token)
    if payload is None:
        raise credentials_exception
        
    user_id: str = payload.get("sub")
    return {"id": user_id} # Aqui você poderia buscar o usuário no DB se necessário