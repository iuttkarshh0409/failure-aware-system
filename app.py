from db.schema import init_db
from services.event_service import detect_event
from db.repositories.event_repo import fetch_latest_event
from services.domain_service import apply_event_to_domain
from services.retry_service import retry_pending_events

init_db()

if __name__ == "__main__":
    detect_event(
        event_type="EVENT_DETECTED",
        payload={
            "message": "this event must survive failure",
            "force_fail": False
        }
    )

    event = fetch_latest_event()

    try:
        apply_event_to_domain(event)
        print("Domain projection succeeded.")
    except Exception as e:
        print("Domain projection failed:", e)

    retry_pending_events()
