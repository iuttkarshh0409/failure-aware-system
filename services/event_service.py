import json
from utils.time import now_iso
from db.repositories.event_repo import insert_event

def detect_event(event_type, payload: dict):
    payload_json = json.dumps(payload, ensure_ascii=False)
    detected_at = now_iso()

    insert_event(
        event_type=event_type,
        payload_json=payload_json,
        detected_at=detected_at
    )
