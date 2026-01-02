from datetime import datetime, timedelta, timezone
from db.connection import get_connection


WINDOW_MINUTES = 10
MIN_EVENTS = 3


def detect_failure_clusters():
    """
    Scan recent FAILED events and persist failure clusters.
    This function is idempotent and safe to re-run.
    """

    conn = get_connection()
    cursor = conn.cursor()

    # 1. Fetch recent FAILED events
    cursor.execute("""
        SELECT event_type, detected_at
        FROM event_detected
        WHERE sync_status = 'FAILED'
        ORDER BY detected_at ASC
    """)

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return 0

    # 2. Group by event_type
    events_by_type = {}
    for event_type, ts in rows:
        ts = datetime.fromisoformat(ts)
        events_by_type.setdefault(event_type, []).append(ts)

    # 3. Detect clusters
    clusters = []

    for event_type, timestamps in events_by_type.items():
        window = []

        for ts in timestamps:
            window.append(ts)

            # remove timestamps outside the window
            cutoff = ts - timedelta(minutes=WINDOW_MINUTES)
            window = [t for t in window if t >= cutoff]

            if len(window) >= MIN_EVENTS:
                clusters.append({
                    "event_type": event_type,
                    "window_start": window[0],
                    "window_end": window[-1],
                    "event_count": len(window)
                })

                # reset window to avoid duplicate clusters
                window = []

    if not clusters:
        return 0

    # 4. Persist clusters
    conn = get_connection()
    cursor = conn.cursor()

    now = datetime.now(timezone.utc).isoformat()

    for c in clusters:
        cursor.execute("""
            INSERT INTO failure_cluster (
                event_type,
                window_start,
                window_end,
                event_count,
                created_at
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            c["event_type"],
            c["window_start"].isoformat(),
            c["window_end"].isoformat(),
            c["event_count"],
            now
        ))

    conn.commit()
    conn.close()

    return len(clusters)
