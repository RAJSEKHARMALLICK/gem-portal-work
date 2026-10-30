
import os
from dotenv import load_dotenv

load_dotenv()


def get_gem_credentials() -> tuple[str, str]:
    """Read GeM credentials from environment variables."""

    cookie = os.getenv("GEM_COOKIE", "")
    csrf_token = os.getenv("GEM_CSRF", "")

    if not cookie or not csrf_token:
        raise ValueError(
            "Missing GEM_COOKIE or GEM_CSRF in .env"
        )

    return cookie, csrf_token
