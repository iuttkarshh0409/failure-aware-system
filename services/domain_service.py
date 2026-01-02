import json
import sqlite3
from db.repositories.domain_repo import insert_domain_projection

def apply_event_to_domain(event_row):
    event_id = event_row[0]
    payload_json = event_row[2]
    detected_at = event_row[3]

    payload = json.loads(payload_json)

    # Simulated failure toggle (keep for now)
    if payload.get("force_fail"):
        raise RuntimeError("Simulated domain failure")

    summary = f"Processed event with payload keys: {list(payload.keys())}"

    try:
        insert_domain_projection(
            event_id=event_id,
            summary=summary,
            created_at=detected_at
        )
    except sqlite3.IntegrityError:
        # Projection already exists → idempotent success
        pass
