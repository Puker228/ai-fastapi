import httpx

from ai.schemas import Prompt
from core.config import settings


class AIClient:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client
        self.url = str(settings.AI_GENERATE_URL)
        self.model = settings.AI_MODEL

    async def generate(self, prompt: str) -> str:
        payload = Prompt(
            model=self.model,
            prompt=prompt,
            stream=False,
        )

        response = await self.client.post(
            self.url,
            json=payload.model_dump(),
        )
        response.raise_for_status()

        return response.json()["response"]
