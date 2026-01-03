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


from utils.backoff import calculate_next_retry

def mark_event_failed(event_id, error_message):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT retry_count
        FROM event_detected
        WHERE id = ?
    """, (event_id,))
    retry_count = cursor.fetchone()[0]

    next_retry_at = calculate_next_retry(retry_count)

    cursor.execute("""
        UPDATE event_detected
        SET sync_status = 'FAILED',
            retry_count = retry_count + 1,
            last_error = ?,
            next_retry_at = ?
        WHERE id = ?
    """, (error_message, next_retry_at, event_id))

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
         SELECT id, event_type, sync_status, retry_count, detected_at, event_note
         FROM event_detected
         ORDER BY id DESC
         LIMIT ?
         """, (limit,))

    rows = cursor.fetchall()
    conn.close()
    return rows

def fetch_health_snapshot():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            COUNT(*) AS total,
            SUM(CASE WHEN sync_status = 'PENDING' THEN 1 ELSE 0 END),
            SUM(CASE WHEN sync_status = 'FAILED' THEN 1 ELSE 0 END),
            SUM(CASE WHEN sync_status = 'DEAD' THEN 1 ELSE 0 END),
            SUM(CASE WHEN sync_status = 'SYNCED' THEN 1 ELSE 0 END)
        FROM event_detected
    """)

    row = cursor.fetchone()

    cursor.execute("""
        SELECT id, detected_at
        FROM event_detected
        WHERE sync_status IN ('PENDING', 'FAILED')
        ORDER BY detected_at
        LIMIT 1
    """)
    oldest = cursor.fetchone()

    cursor.execute("""
        SELECT id, retry_count
        FROM event_detected
        ORDER BY retry_count DESC
        LIMIT 1
    """)
    most_retried = cursor.fetchone()

    conn.close()

    return {
        "total": row[0],
        "pending": row[1],
        "failed": row[2],
        "dead": row[3],
        "synced": row[4],
        "oldest_unresolved": oldest,
        "most_retried": most_retried,
    }

def add_event_note(event_id, note):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE event_detected
        SET event_note = ?
        WHERE id = ?
    """, (note, event_id))

    conn.commit()
    conn.close()


def fetch_event_note(event_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT event_note
        FROM event_detected
        WHERE id = ?
    """, (event_id,))

    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def fetch_failure_clusters(limit=10):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            event_type,
            window_start,
            window_end,
            event_count,
            created_at
        FROM failure_cluster
        ORDER BY created_at DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()
    return rows

def fetch_failed_events(): #added on my own
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, retry_count
        FROM event_detected
        WHERE sync_status = 'FAILED'
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows

def fetch_dead_events(): #added on my own
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id
        FROM event_detected
        WHERE sync_status = 'DEAD'
    """)

    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]

