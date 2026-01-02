from db.connection import get_connection

def insert_domain_projection(event_id, summary, created_at):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO domain_state (
            event_id,
            summary,
            created_at
        )
        VALUES (?, ?, ?)
    """, (event_id, summary, created_at))

    conn.commit()
    conn.close()
