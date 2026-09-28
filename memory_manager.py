import os
import requests
from dotenv import load_dotenv

load_dotenv()

class HindsightMemoryManager:
    def __init__(self):
        self.api_key = os.getenv("HINDSIGHT_API_KEY")
        self.base_url = os.getenv("HINDSIGHT_BASE_URL", "https://api.hindsight.vectorize.io").rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def retain(self, bank_id: str, content: str, context: str = "meeting_notes") -> bool:
        """Saves an interaction or constraint into Hindsight's memory bank."""
        url = f"{self.base_url}/v1/banks/{bank_id}/memories"
        payload = {
            "content": content,
            "metadata": {"context": context}
        }
        try:
            resp = requests.post(url, json=payload, headers=self.headers, timeout=10)
            return resp.status_code in [200, 201]
        except Exception as e:
            print(f"[Hindsight Retain Error]: {e}")
            return False

    def recall(self, bank_id: str, query: str, limit: int = 5) -> list:
        """Retrieves raw semantic memories from Hindsight."""
        url = f"{self.base_url}/v1/banks/{bank_id}/memories/search"
        payload = {"query": query, "limit": limit}
        try:
            resp = requests.post(url, json=payload, headers=self.headers, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                return [item.get("content", "") for item in data.get("memories", [])]
        except Exception as e:
            print(f"[Hindsight Recall Error]: {e}")
        return []

    def reflect(self, bank_id: str, query: str) -> str:
        """Synthesizes high-level rules, objections, and negotiation guardrails."""
        url = f"{self.base_url}/v1/banks/{bank_id}/reflect"
        payload = {"query": query}
        try:
            resp = requests.post(url, json=payload, headers=self.headers, timeout=12)
            if resp.status_code == 200:
                return resp.json().get("reflection", "No high-level patterns formed yet.")
        except Exception as e:
            print(f"[Hindsight Reflect Error]: {e}")
        return "Recall fallback: Analyze raw constraints."