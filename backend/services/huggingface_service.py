import logging
import httpx
from config import settings

logger = logging.getLogger(__name__)

class HuggingFaceService:
    def __init__(self):
        self.api_key = settings.HUGGINGFACE_API_KEY
        # Router API URL for HF Inference
        self.model_url = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    async def categorize_urban_issue(self, text: str) -> dict:
        """
        Performs live zero-shot classification via Hugging Face Inference API.
        No local fallback data used.
        """
        if not self.api_key:
            raise ValueError("Hugging Face API key is missing in .env file.")

        payload = {
            "inputs": text,
            "parameters": {
                "candidate_labels": [
                    "Air Pollution / Smog", 
                    "Waste Management", 
                    "Water Quality", 
                    "Infrastructure Damage", 
                    "Traffic / Noise"
                ]
            }
        }

        # Follow redirects & enable custom limits to handle Windows DNS resolution reliably
        transport = httpx.AsyncHTTPTransport(retries=3)
        async with httpx.AsyncClient(transport=transport, timeout=30.0, follow_redirects=True) as client:
            try:
                response = await client.post(self.model_url, headers=self.headers, json=payload)
                response.raise_for_status()
                return response.json()
            except httpx.RequestError as exc:
                logger.error(f"Hugging Face Live Network Error: {exc}")
                raise RuntimeError(f"Hugging Face network call failed: {exc}")
            except httpx.HTTPStatusError as exc:
                logger.error(f"Hugging Face HTTP Error ({exc.response.status_code}): {exc.response.text}")
                raise RuntimeError(f"Hugging Face API returned status {exc.response.status_code}: {exc.response.text}")