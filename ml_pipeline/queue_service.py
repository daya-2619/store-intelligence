import time

from state_manager import (
    track_positions,
    queue_state
)


QUEUE_TIME = 15


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
        ][-50:]
    )

    if len(positions) < 50:
        return False

    first = positions[0]
    last = positions[-1]

    movement = (
        (
            last[0] - first[0]
        ) ** 2
        +
        (
            last[1] - first[1]
        ) ** 2
    ) ** 0.5

    duration = (
        last[2] - first[2]
    )

    if (
        movement < 25
        and
        duration > QUEUE_TIME
    ):
        return True

    return False