# src/ollama_client.py
import httpx
from .config import Config

class OllamaClient:
    def __init__(self, config: Config):
        self.config = config

    def generate_review(self, prompt: str):
        url = f"{self.config.api_base}/api/generate"
        payload = {
            "model": self.config.model,
            "prompt": prompt,
            "stream": False
        }
        response = httpx.post(url, json=payload, timeout=300.0)
        response.raise_for_status()
        return response.json()["response"]