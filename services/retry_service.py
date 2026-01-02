from db.connection import get_connection
from services.sync_service import try_sync_event
from db.repositories.event_repo import (
    mark_event_synced,
    mark_event_failed
)

MAX_RETRIES = 5

def mark_event_dead(event_id, error_message):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE event_detected
        SET sync_status = 'DEAD',
            last_error = ?
        WHERE id = ?
    """, (error_message, event_id))

    conn.commit()
    conn.close()

from datetime import datetime, timezone

def retry_pending_events():
    conn = get_connection()
    cursor = conn.cursor()

    now = datetime.now(timezone.utc).isoformat()

    cursor.execute("""
        SELECT id, event_type, event_payload, detected_at, sync_status, retry_count, next_retry_at
        FROM event_detected
        WHERE sync_status IN ('PENDING', 'FAILED')
          AND (next_retry_at IS NULL OR next_retry_at <= ?)
        ORDER BY id
    """, (now,))

    events = cursor.fetchall()
    conn.close()

    for event in events:
        event_id = event[0]
        retry_count = event[5]

        if retry_count >= MAX_RETRIES:
            mark_event_dead(event_id, "Max retries exceeded")
            continue

        try:
            try_sync_event(event)
            mark_event_synced(event_id)
        except Exception as e:
            mark_event_failed(event_id, str(e))
