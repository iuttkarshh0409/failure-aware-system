from db.connection import get_connection
from services.sync_service import try_sync_event
from db.repositories.event_repo import (
    mark_event_synced,
    mark_event_failed
)

MAX_RETRIES = 5

def retry_pending_events():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, event_type, event_payload, detected_at, sync_status, retry_count
        FROM event_detected
        WHERE sync_status IN ('PENDING', 'FAILED')
          AND retry_count < ?
        ORDER BY id
    """, (MAX_RETRIES,))

    events = cursor.fetchall()
    conn.close()

    for event in events:
        event_id = event[0]
        try:
            try_sync_event(event)
            mark_event_synced(event_id)
        except Exception as e:
            mark_event_failed(event_id, str(e))
