import requests
import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

class EventRouter:
    @staticmethod
    def route_event(event_data: Dict[str, Any]):
        try:
            response = requests.post(
                f"{API_BASE_URL}/events/ingest",
                json=[event_data],
                timeout=2.0
            )
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            print(f"Failed to route event: {e}")
            return False
