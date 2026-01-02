from datetime import timedelta
from utils.time import now_iso
from datetime import datetime, timezone

def calculate_next_retry(retry_count):
    if retry_count == 0:
        delay = timedelta(seconds=10)
    elif retry_count == 1:
        delay = timedelta(seconds=30)
    elif retry_count == 2:
        delay = timedelta(minutes=2)
    else:
        delay = timedelta(minutes=10)

    next_time = datetime.now(timezone.utc) + delay
    return next_time.isoformat()
