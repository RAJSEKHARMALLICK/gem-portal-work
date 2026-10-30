
from datetime import datetime, timezone


def format_deadline(date_string: str) -> str:
    """Format a GeM deadline and show calendar days remaining."""

    deadline = datetime.fromisoformat(
        date_string.replace("Z", "+00:00")
    )

    # Convert to Indian Standard Time
    ist = timezone.utc
    from datetime import timedelta
    ist = timezone(timedelta(hours=5, minutes=30))

    local_deadline = deadline.astimezone(ist)
    today = datetime.now(ist).date()

    days_left = (local_deadline.date() - today).days

    formatted_date = local_deadline.strftime("%d-%B-%Y")

    if days_left < 0:
        return f"{formatted_date} (Expired)"
    elif days_left == 0:
        return f"{formatted_date} (Last day)"
    elif days_left == 1:
        return f"{formatted_date} (1 day left)"

    return f"{formatted_date} ({days_left} days left)"
