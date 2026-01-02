from db.connection import get_connection

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS event_detected (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_type TEXT NOT NULL,
        event_payload TEXT NOT NULL,
        detected_at TEXT NOT NULL,
        sync_status TEXT NOT NULL DEFAULT 'PENDING',
        retry_count INTEGER NOT NULL DEFAULT 0,
        last_error TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS domain_state (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_id INTEGER NOT NULL,
        summary TEXT NOT NULL,
        created_at TEXT NOT NULL,
        UNIQUE(event_id)
    );
    """)

    conn.commit()
    conn.close()

    migrate_event_detected()
    init_correlation_schema()


def migrate_event_detected():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(event_detected);")
    columns = {row[1] for row in cursor.fetchall()}

    if "next_retry_at" not in columns:
        cursor.execute(
            "ALTER TABLE event_detected ADD COLUMN next_retry_at TEXT;"
        )

    if "event_note" not in columns:
        cursor.execute(
            "ALTER TABLE event_detected ADD COLUMN event_note TEXT;"
        )

    conn.commit()
    conn.close()

def init_correlation_schema():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS failure_cluster (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_type TEXT NOT NULL,
        window_start TEXT NOT NULL,
        window_end TEXT NOT NULL,
        event_count INTEGER NOT NULL,
        created_at TEXT NOT NULL
    );
    """)

    conn.commit()
    conn.close()

