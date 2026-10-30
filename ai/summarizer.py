
import requests

from ai.prompts import TENDER_SUMMARY_PROMPT


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma3:4b"


def summarize_tender(tender_text: str) -> str:
    """Summarize technical tender scope using local Ollama."""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "system": TENDER_SUMMARY_PROMPT,
            "prompt": (
                "Identify the actual technical work described "
                "in the following GeM tender.\n\n"
                f"{tender_text}"
            ),
            "stream": False,
            "options": {
                "temperature": 0.1,
                "num_ctx": 16384,
                "num_predict": 300,
            },
        },
        timeout=600,
    )

    response.raise_for_status()

    return response.json()["response"].strip()

