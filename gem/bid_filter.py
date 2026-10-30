
from datetime import datetime, timezone


def filter_active_bids(bids: list[dict]) -> list[dict]:
    """Return bids whose submission deadlines are in the future."""

    now = datetime.now(timezone.utc)
    active_bids = []

    for bid in bids:
        end_dates = bid.get("final_end_date_sort", [])

        if not end_dates:
            continue

        end_date = datetime.fromisoformat(
            end_dates[0].replace("Z", "+00:00")
        )

        if end_date > now:
            active_bids.append(bid)

    return active_bids
