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
