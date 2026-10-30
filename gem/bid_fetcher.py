
from requests import Session

from gem.client import search_bids


def fetch_all_bids(
    session: Session,
    base_payload: dict
) -> list[dict]:
    """Fetch all matching bids across GeM search result pages."""

    all_bids = []
    seen_ids = set()
    page = 1

    while True:
        # Prepare search criteria for the current page
        payload = {**base_payload, "page": page}

        # Fetch one page from GeM
        result = search_bids(session, payload)

        data = result["response"]["response"]
        bids = data["docs"]
        total = data["numFound"]

        if not bids:
            break

        # Avoid duplicate bids
        for bid in bids:
            bid_id = bid["id"]

            if bid_id not in seen_ids:
                all_bids.append(bid)
                seen_ids.add(bid_id)

        print(f"Page {page}: {len(bids)} bids fetched")

        # Stop after collecting all matching bids
        if len(all_bids) >= total:
            break

        page += 1

    return all_bids
