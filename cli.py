from db.schema import init_db
from db.repositories.event_repo import fetch_health_snapshot
from db.repositories.event_repo import add_event_note
from db.repositories.event_repo import fetch_failure_clusters
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
        event_id, event_type, status, retries, ts, note = e

        print(
            f"#{event_id:<3} | "
            f"{event_type:<15} | "
            f"{status:<7} | "
            f"retries={retries:<2} | "
            f"{ts}"
        )

        if note:
            print(f"        note: {note}")


def show_health():
    snapshot = fetch_health_snapshot()

    print("\nSystem Health")
    print("-" * 20)

    print(f"Total events : {snapshot['total']}")
    print(f"Pending      : {snapshot['pending']}")
    print(f"Failed       : {snapshot['failed']}")
    print(f"Dead         : {snapshot['dead']}")
    print(f"Synced       : {snapshot['synced']}")

    if snapshot["oldest_unresolved"]:
        eid, ts = snapshot["oldest_unresolved"]
        print(f"\nOldest unresolved event : #{eid} @ {ts}")
    else:
        print("\nOldest unresolved event : none")

    if snapshot["most_retried"]:
        eid, retries = snapshot["most_retried"]
        print(f"Most retries            : #{eid} ({retries} retries)")
    else:
        print("Most retries            : none")

def show_clusters():
    clusters = fetch_failure_clusters()

    print("\nFailure Clusters")
    print("-" * 20)

    if not clusters:
        print("No failure clusters detected.")
        return

    for c in clusters:
        event_type, start, end, count, created_at = c

        print(f"{event_type}")
        print(f"  events : {count}")
        print(f"  window : {start} → {end}")
        print()


def main():
    init_db
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

    parser.add_argument(
    "--health",
    action="store_true",
    help="Show system health diagnostics"
)

    parser.add_argument(
    "--annotate",
    nargs=2,
    metavar=("EVENT_ID", "NOTE"),
    help="Attach a human-readable note to an event"
    )

    parser.add_argument(
    "--clusters",
    action="store_true",
    help="Show detected failure clusters"
)



    args = parser.parse_args()

    if args.health:
        show_health()


    if args.status:
        show_status()

    if args.recent:
        show_recent(args.recent)

    if not (args.status or args.recent or args.health or args.annotate or args.clusters):
       parser.print_help()



    if args.annotate:
       event_id = int(args.annotate[0])
       note = args.annotate[1]
       add_event_note(event_id, note)
       print(f"Note added to event #{event_id}")

    if args.clusters:
       show_clusters()



if __name__ == "__main__":
    main()
