
import os

from dotenv import load_dotenv
from openai import OpenAI

from ai.prompts import TENDER_SUMMARY_PROMPT


def summarize_tender(tender_text: str) -> str:
    """Generate a short technical tender summary."""

    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY missing from .env")

    client = OpenAI(api_key=api_key)

    response = client.responses.create(
        model="gpt-4.1-mini",
        instructions=TENDER_SUMMARY_PROMPT,
        input=tender_text,
        max_output_tokens=350,
    )

    return response.output_text.strip()
