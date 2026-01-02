import random

def try_sync_event(event_row):
    """
    Simulates syncing to an external system.
    Randomly fails to mimic real-world behavior.
    """
    if random.random() < 0.6:
        raise RuntimeError("Simulated external sync failure")

    return True
