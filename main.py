
from gem.client import create_session
from gem.bid_fetcher import fetch_all_bids
from gem.bid_filter import filter_active_bids
from output.date_formatter import format_deadline


def main():
    # Search criteria
    payload = {
        "searchType": "ministry-search",
        "ministry": "Ministry of Steel",
        "buyerState": "",
        "organization": "Rourkela Steel Plant",
        "department": "",
        "bidEndFromMin": "",
        "bidEndToMin": "",
    }

    # Fetch all bids using an anonymous GeM session
    with create_session() as session:
        bids = fetch_all_bids(session, payload)

    # Keep only bids whose submission deadlines haven't passed
    active_bids = filter_active_bids(bids)

    # Display summary
    print(f"\nTotal unique bids fetched: {len(bids)}")
    print(f"Active bids: {len(active_bids)}")

    print("\n--- Active GeM Bids ---")

    for bid in active_bids:
        bid_id = bid["id"]
        bid_number = bid.get("b_bid_number", ["Unknown"])[0]
        end_date = bid.get("final_end_date_sort", ["Unknown"])[0]

        print(f"ID: {bid_id}")
        print(f"Bid: {bid_number}")
        print(f"Deadline: {format_deadline(end_date)}")
        print("-" * 40)


if __name__ == "__main__":
    main()
