from datetime import datetime, timezone

from db.connection import get_connection
from db.repositories.event_repo import (
    fetch_failed_events,
    fetch_dead_events
)
from db.repositories.cluster_repo import fetch_failure_clusters


SEVERITY_LOW = "LOW"
SEVERITY_MEDIUM = "MEDIUM"
SEVERITY_HIGH = "HIGH"
SEVERITY_CRITICAL = "CRITICAL"


def recompute_severity():
    """
    Recomputes severity snapshot from current system state.
    This table is disposable and fully derived.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Clear previous snapshot
    cursor.execute("DELETE FROM failure_severity;")

    now = datetime.now(timezone.utc).isoformat()

    _severity_for_events(cursor, now)
    _severity_for_clusters(cursor, now)

    conn.commit()
    conn.close()

def _severity_for_events(cursor, now):
    failed_events = fetch_failed_events()
    dead_events = fetch_dead_events()

    # FAILED events
    for event in failed_events:
        event_id, retry_count = event

        if retry_count >= 3:
            severity = SEVERITY_MEDIUM
            reason = "Event has failed repeatedly and is nearing retry exhaustion"
        else:
            severity = SEVERITY_LOW
            reason = "Isolated failure, retries still available"

        cursor.execute("""
            INSERT INTO failure_severity
            (entity_type, entity_id, severity, reason, computed_at)
            VALUES (?, ?, ?, ?, ?)
        """, ("event", event_id, severity, reason, now))

    # DEAD events
    for event_id in dead_events:
        cursor.execute("""
            INSERT INTO failure_severity
            (entity_type, entity_id, severity, reason, computed_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            "event",
            event_id,
            SEVERITY_HIGH,
            "Event exhausted retries and entered DEAD state",
            now
        ))

def _severity_for_clusters(cursor, now):
    clusters = fetch_failure_clusters()

    for cluster in clusters:
        cluster_id, size, recurring = cluster

        if recurring:
            severity = SEVERITY_CRITICAL
            reason = "Recurring failure cluster detected across multiple cycles"
        elif size >= 3:
            severity = SEVERITY_HIGH
            reason = "Multiple failures clustered together"
        else:
            severity = SEVERITY_MEDIUM
            reason = "Small but notable failure cluster"

        cursor.execute("""
            INSERT INTO failure_severity
            (entity_type, entity_id, severity, reason, computed_at)
            VALUES (?, ?, ?, ?, ?)
        """, ("cluster", cluster_id, severity, reason, now))

