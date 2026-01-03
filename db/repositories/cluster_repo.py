from db.connection import get_connection


def fetch_failure_clusters():
    """
    Groups failures by event_type and recent time window.
    Returns:
    [(cluster_id, size, recurring), ...]
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            MIN(id) AS cluster_id,
            COUNT(*) AS cluster_size,
            CASE
                WHEN COUNT(*) >= 5 THEN 1
                ELSE 0
            END AS recurring
        FROM event_detected
        WHERE sync_status IN ('FAILED', 'DEAD')
        GROUP BY event_type
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows