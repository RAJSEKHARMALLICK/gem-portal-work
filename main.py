
import argparse
from datetime import datetime

from gem.client import create_session
from gem.bid_fetcher import fetch_all_bids
from gem.bid_filter import filter_active_bids

from pdf.pdf_fetcher import fetch_bid_pdf
from pdf.pdf_extractor import extract_pdf_text

from ai.summarizer import summarize_tender
from output.date_formatter import format_deadline


BASE_URL = "https://bidplus.gem.gov.in"


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Summarize active Rourkela Steel Plant GeM bids"
    )

    parser.add_argument(
        "--top",
        type=int,
        default=3,
        help="Number of bids to summarize (default: 3)"
    )

    args = parser.parse_args()

    if args.top < 1:
        parser.error("--top must be greater than zero")

    return args


def get_deadline(bid: dict) -> datetime:
    """Return the bid's submission deadline."""

    end_date = bid["final_end_date_sort"][0]

    return datetime.fromisoformat(
        end_date.replace("Z", "+00:00")
    )


def main():
    args = parse_arguments()

    payload = {
        "searchType": "ministry-search",
        "ministry": "Ministry of Steel",
        "buyerState": "",
        "organization": "Rourkela Steel Plant",
        "department": "",
        "bidEndFromMin": "",
        "bidEndToMin": "",
    }

    processed = 0
    skipped_invalid_pdf = 0
    skipped_other = 0

    with create_session() as session:

        # Fetch bids across all pages
        bids = fetch_all_bids(session, payload)

        # Keep only active bids
        active_bids = filter_active_bids(bids)

        # Sort by nearest submission deadline
        active_bids.sort(key=get_deadline)

        print(f"\nTotal unique bids: {len(bids)}")
        print(f"Active bids: {len(active_bids)}")
        print(f"Requested summaries: {args.top}")
        print("Sort order: Earliest deadline first\n")

        for bid in active_bids:

            # Stop after successfully summarizing N bids
            if processed >= args.top:
                break

            bid_id = bid["id"]

            bid_number = bid.get(
                "b_bid_number", ["Unknown"]
            )[0]

            end_date = bid["final_end_date_sort"][0]

            pdf_url = (
                f"{BASE_URL}/showbidDocument/{bid_id}"
            )

            # Fetch tender PDF into memory
            try:
                pdf_bytes = fetch_bid_pdf(
                    session,
                    bid_id
                )

            except ValueError as error:
                if "Invalid PDF response" in str(error):
                    skipped_invalid_pdf += 1
                    continue

                skipped_other += 1
                print(f"Error fetching {bid_number}: {error}")
                continue

            except Exception as error:
                skipped_other += 1
                print(f"Error fetching {bid_number}: {error}")
                continue

            # Extract PDF text
            try:
                tender_text = extract_pdf_text(pdf_bytes)

                if not tender_text.strip():
                    skipped_other += 1
                    continue

                # Summarize using local Ollama
                summary = summarize_tender(tender_text)

                if not summary.strip():
                    skipped_other += 1
                    continue

            except Exception as error:
                skipped_other += 1
                print(f"Error processing {bid_number}: {error}")
                continue

            processed += 1

            print("=" * 70)
            print(f"Bid {processed}/{args.top}")
            print(f"Bid Number: {bid_number}")
            print(f"Deadline: {format_deadline(end_date)}")
            print(f"PDF: {pdf_url}")
            print("\nTechnical Summary:")
            print(summary)
            print()

    print("=" * 70)
    print("Processing completed.")
    print(f"Successfully summarized: {processed}")
    print(f"Skipped invalid PDFs: {skipped_invalid_pdf}")
    print(f"Skipped other errors: {skipped_other}")


if __name__ == "__main__":
    main()
