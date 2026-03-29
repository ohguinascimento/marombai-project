import os
import json
import httpx
from typing import Optional, Dict, Any
from loguru import logger
from fastapi import HTTPException

class AIService:
    def __init__(self):
        self.user = os.getenv("N8N_USER", "admin")
        self.password = os.getenv("N8N_PASSWORD", "marombai_n8n_secure")
        self.url_treino = os.getenv("WEBHOOK_URL", "http://n8n:5678/webhook-test/gerar-treino")
        self.url_dieta = os.getenv("WEBHOOK_URL_DIETA", "http://n8n:5678/webhook/gerar-dieta")
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
                    logger.error(f"❌ Erro na resposta do n8n: {response.status_code} - {response.text}")
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
                # Remove blocos de código markdown se existirem
                clean_json = content.replace("```json", "").replace("```", "").strip()
                return json.loads(clean_json)
            except json.JSONDecodeError:
                logger.error(f"❌ Falha ao parsear JSON da IA na chave {key}")
                return None
        
        return content

    async def generate_workout(self, nome: str, perfil: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Orquestra a geração de treino via n8n."""
        logger.info(f"📡 Solicitando inteligência de treino para: {nome}")
        payload = {"nome": nome, "perfil": perfil}
        
        res = await self._post_request(self.url_treino, payload)
        if res:
            return self._parse_ai_json(res, "treino")
        return None

    async def generate_diet(self, user_data: Dict[str, Any], diet_profile: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Orquestra a geração de dieta via n8n."""
        logger.info(f"📡 Solicitando inteligência de dieta")
        payload = {"user": user_data, "perfil_dieta": diet_profile}
        
        res = await self._post_request(self.url_dieta, payload)
        if res:
            return self._parse_ai_json(res, "dieta")
        return None