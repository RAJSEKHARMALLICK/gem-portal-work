


import json
import requests

BASE_URL = "https://bidplus.gem.gov.in"


def create_session() -> requests.Session:
    """Start an anonymous GeM session."""

    session = requests.Session()

    session.headers.update({
        "User-Agent": "Mozilla/5.0",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": f"{BASE_URL}/advance-search",
    })

    response = session.get(
        f"{BASE_URL}/advance-search",
        timeout=30,
    )

    response.raise_for_status()

    return session


def search_bids(
    session: requests.Session,
    payload: dict
) -> dict:
    """Search GeM bids using the anonymous session."""

    csrf_token = session.cookies.get("csrf_gem_cookie")

    if not csrf_token:
        raise ValueError("GeM CSRF cookie not found")

    response = session.post(
        f"{BASE_URL}/search-bids",
        data={
            "payload": json.dumps(payload),
            "csrf_bd_gem_nk": csrf_token,
        },
        timeout=30,
    )

    response.raise_for_status()

    result = response.json()

    if result.get("status") != 1:
        raise ValueError(f"GeM API error: {result}")

    return result
