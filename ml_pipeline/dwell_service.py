import time

from state_manager import (
    zone_entry_time
)


def track_dwell(
    visitor_id,
    zone
):

    now = time.time()

    key = (
        visitor_id,
        zone
    )

    if key not in zone_entry_time:

        zone_entry_time[key] = now

        return None

    dwell_ms = int(
        (
            now -
            zone_entry_time[key]
        ) * 1000
    )

    return dwell_ms