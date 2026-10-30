
import requests


BASE_URL = "https://bidplus.gem.gov.in"


def fetch_bid_pdf(
    session: requests.Session,
    bid_id: str
) -> bytes:
    """Fetch a GeM tender PDF into memory."""

    url = f"{BASE_URL}/showbidDocument/{bid_id}"

    response = session.get(
        url,
        timeout=60,
    )

    response.raise_for_status()

    pdf_bytes = response.content

    if not pdf_bytes.startswith(b"%PDF-"):
        raise ValueError(
            f"Invalid PDF response for bid ID: {bid_id}"
        )

    return pdf_bytes
