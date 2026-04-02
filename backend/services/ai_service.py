import json
import httpx
from typing import Optional, Dict, Any
from loguru import logger
from fastapi import HTTPException
from backend.config import settings
from backend.services.ai_schemas import UserDataSchema, DietProfileSchema, WorkoutProfileSchema

class AIService:
    def __init__(self):
        """
        Inicializa o serviço de IA. 
        As validações de credenciais agora são feitas globalmente no config.py.
        """
        self.user = settings.N8N_USER
        self.password = settings.N8N_PASSWORD
        self.url_treino = settings.WEBHOOK_URL_TREINO
        self.url_dieta = settings.WEBHOOK_URL_DIETA
        self.timeout = 60.0

    def _make_json_serializable(self, data: Any) -> Any:
        """Converte recursivamente objetos datetime/date em strings ISO."""
        if isinstance(data, dict):
            return {k: self._make_json_serializable(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._make_json_serializable(v) for v in data]
        elif hasattr(data, "isoformat"):
            return data.isoformat()
        return data

    async def _post_request(self, url: str, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Método privado para realizar as chamadas HTTP assíncronas."""
        # Garante que o payload não tenha objetos que quebrem o JSON (como datetime)
        safe_payload = self._make_json_serializable(payload)
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    url,
                    json=safe_payload,
                    timeout=self.timeout,
                    auth=(self.user, self.password)
                )
                
                if response.status_code != 200:
                    logger.error(f"❌ n8n retornou erro {response.status_code}")
                    return None
                
                return response.json()
            except Exception as e:
                logger.error(f"❌ Falha de conexão com o serviço de IA: {str(e)}")
                return None

    def _parse_ai_json(self, data: Any, key: str) -> Optional[Dict[str, Any]]:
        """Limpa e converte strings formatadas em JSON caso a IA envie Markdown."""
        content = data.get(key)
        if not content:
            return None
            
        if isinstance(content, str):
            try:
                # Regex ou substituição mais agressiva para limpar markdown da IA
                import re
                json_match = re.search(r'(\{.*\}|\[.*\])', content, re.DOTALL)
                return json.loads(json_match.group(0)) if json_match else None
            except json.JSONDecodeError:
                logger.error(f"❌ Falha ao parsear JSON da IA na chave {key}")
                return None
        
        return content

    async def generate_workout(self, user: UserDataSchema, perfil: WorkoutProfileSchema) -> Optional[Dict[str, Any]]:
        """Orquestra a geração de treino via n8n."""
        logger.info(f"📡 Solicitando inteligência de treino para: {user.nome}")
        payload = {
            "user": user.model_dump(mode='json'),
            "perfil_treino": perfil.model_dump(mode='json')
        }
        
        res = await self._post_request(self.url_treino, payload)
        if res:
            return self._parse_ai_json(res, "treino")
        return None

    async def generate_diet(self, user: UserDataSchema, diet_profile: DietProfileSchema) -> Optional[Dict[str, Any]]:
        """Orquestra a geração de dieta via n8n."""
        logger.info(f"📡 Solicitando inteligência de dieta para: {user.nome}")
        payload = {
            "user": user.model_dump(mode='json'),
            "perfil_dieta": diet_profile.model_dump(mode='json')
        }
        
        res = await self._post_request(self.url_dieta, payload)
        if res:
            return self._parse_ai_json(res, "dieta")
        return None