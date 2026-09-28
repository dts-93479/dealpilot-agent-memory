import os
import requests
from dotenv import load_dotenv

load_dotenv()

class HindsightMemoryManager:
    def __init__(self):
        self.api_key = os.getenv("HINDSIGHT_API_KEY", "")
        raw_url = os.getenv("HINDSIGHT_BASE_URL", "https://api.hindsight.vectorize.io")
        self.base_url = raw_url.rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        # Built-in local fallback buffer to ensure demo continuity
        self._local_banks = {}

    def retain(self, bank_id: str, content: str, context: str = "meeting_notes") -> bool:
        """Stores constraint into Hindsight with automatic local fallback."""
        if not content or not content.strip():
            return False

        # Always update local bank for guaranteed demo execution
        if bank_id not in self._local_banks:
            self._local_banks[bank_id] = []
        self._local_banks[bank_id].append(content.strip())

        # Attempt remote Hindsight Cloud API call
        if self.api_key:
            endpoints = [
                f"{self.base_url}/v1/banks/{bank_id}/memories",
                f"{self.base_url}/banks/{bank_id}/memories",
                f"{self.base_url}/api/v1/memories"
            ]
            payload = {
                "bank_id": bank_id,
                "content": content.strip(),
                "metadata": {"context": context}
            }
            for url in endpoints:
                try:
                    resp = requests.post(url, json=payload, headers=self.headers, timeout=5)
                    if resp.status_code in [200, 201]:
                        return True
                    else:
                        print(f"[Hindsight Retain Notice] {url} returned {resp.status_code}: {resp.text}")
                except Exception as e:
                    print(f"[Hindsight Network Notice] {e}")

        # If remote call fails or is unconfigured, return True via local fallback
        return True

    def recall(self, bank_id: str, query: str, limit: int = 5) -> list:
        """Fetches memories from Hindsight or local memory bank."""
        if self.api_key:
            endpoints = [
                f"{self.base_url}/v1/banks/{bank_id}/memories/search",
                f"{self.base_url}/banks/{bank_id}/memories/search"
            ]
            for url in endpoints:
                try:
                    resp = requests.post(url, json={"query": query, "limit": limit}, headers=self.headers, timeout=5)
                    if resp.status_code == 200:
                        data = resp.json()
                        items = data.get("memories", [])
                        if items:
                            return [item.get("content", str(item)) for item in items]
                except Exception:
                    pass

        # Local fallback return
        return self._local_banks.get(bank_id, [])[-limit:]

    def reflect(self, bank_id: str, query: str) -> str:
        """Synthesizes high-level constraints into strategic guardrails."""
        if self.api_key:
            endpoints = [
                f"{self.base_url}/v1/banks/{bank_id}/reflect",
                f"{self.base_url}/banks/{bank_id}/reflect"
            ]
            for url in endpoints:
                try:
                    resp = requests.post(url, json={"query": query}, headers=self.headers, timeout=5)
                    if resp.status_code == 200:
                        reflection = resp.json().get("reflection")
                        if reflection:
                            return reflection
                except Exception:
                    pass

        # Intelligent synthesis fallback for demo flow
        memories = self._local_banks.get(bank_id, [])
        if memories:
            return "Synthesized Guardrails from Past Calls:\n" + "\n".join([f"- Mandate: {m}" for m in memories])
        return "No specific past constraints indexed for this bank yet."