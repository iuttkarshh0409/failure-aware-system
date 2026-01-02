from db.connection import get_connection

def insert_event(event_type, payload_json, detected_at):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO event_detected (
            event_type,
            event_payload,
            detected_at
        )
        VALUES (?, ?, ?)
    """, (event_type, payload_json, detected_at))

    conn.commit()
    conn.close()

def fetch_latest_event():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, event_type, event_payload, detected_at, sync_status
        FROM event_detected
        ORDER BY id DESC
        LIMIT 1
    """)

    row = cursor.fetchone()
    conn.close()
    return row

def mark_event_synced(event_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE event_detected
        SET sync_status = 'SYNCED'
        WHERE id = ?
    """, (event_id,))

    conn.commit()
    conn.close()


def mark_event_failed(event_id, error_message):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE event_detected
        SET sync_status = 'FAILED',
            retry_count = retry_count + 1,
            last_error = ?
        WHERE id = ?
    """, (error_message, event_id))

    conn.commit()
    conn.close()

def fetch_event_counts():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT sync_status, COUNT(*)
        FROM event_detected
        GROUP BY sync_status
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows


def fetch_recent_events(limit=10):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, event_type, sync_status, retry_count, detected_at
        FROM event_detected
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()
    return rows
