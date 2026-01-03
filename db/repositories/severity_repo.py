from db.connection import get_connection


def fetch_severity_snapshot():
    """
    Returns severity distribution across entities.
    Output:
    [(severity, count), ...]
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT severity, COUNT(*)
        FROM failure_severity
        GROUP BY severity
        ORDER BY
            CASE severity
                WHEN 'CRITICAL' THEN 1
                WHEN 'HIGH' THEN 2
                WHEN 'MEDIUM' THEN 3
                WHEN 'LOW' THEN 4
                ELSE 5
            END
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows
