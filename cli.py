import argparse
from db.repositories.event_repo import (
    fetch_event_counts,
    fetch_recent_events
)

def show_status():
    print("\nSystem Status\n" + "-" * 20)

    counts = fetch_event_counts()
    if not counts:
        print("No events found.")
        return

    for status, count in counts:
        print(f"{status:10} : {count}")

def show_recent(limit):
    print(f"\nLast {limit} Events\n" + "-" * 20)

    events = fetch_recent_events(limit)
    if not events:
        print("No events found.")
        return

    for e in events:
        event_id, event_type, status, retries, ts = e
        print(
            f"#{event_id:<3} | "
            f"{event_type:<15} | "
            f"{status:<7} | "
            f"retries={retries:<2} | "
            f"{ts}"
        )

def main():
    parser = argparse.ArgumentParser(
        description="Failure-Aware System CLI (read-only)"
    )

    parser.add_argument(
        "--status",
        action="store_true",
        help="Show system health summary"
    )

    parser.add_argument(
        "--recent",
        type=int,
        metavar="N",
        help="Show last N events"
    )

    args = parser.parse_args()

    if args.status:
        show_status()

    if args.recent:
        show_recent(args.recent)

    if not args.status and not args.recent:
        parser.print_help()

if __name__ == "__main__":
    main()
