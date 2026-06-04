import time

from state_manager import (
    zone_entry_time,
    track_positions,
    queue_state,
    heatmap_points
)


def update_heatmap(x, y):

    heatmap_points.append(
        (x, y)
    )


def calculate_dwell(
    visitor_id,
    zone
):

    key = (
        visitor_id,
        zone
    )

    now = time.time()

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


def detect_queue(
    visitor_id,
    x,
    y
):

    now = time.time()

    if visitor_id not in track_positions:

        track_positions[
            visitor_id
        ] = []

    track_positions[
        visitor_id
    ].append(
        (
            x,
            y,
            now
        )
    )

    positions = (
        track_positions[
            visitor_id
        ][-30:]
    )

    if len(positions) < 30:
        return False

    start_x = positions[0][0]
    start_y = positions[0][1]

    end_x = positions[-1][0]
    end_y = positions[-1][1]

    movement = (
        (end_x - start_x) ** 2
        +
        (end_y - start_y) ** 2
    ) ** 0.5

    return movement < 25