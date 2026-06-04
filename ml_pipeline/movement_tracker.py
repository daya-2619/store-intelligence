track_points = {}

def save_point(
    visitor_id,
    x,
    y
):

    if visitor_id not in track_points:
        track_points[visitor_id] = []

    track_points[visitor_id].append(
        (int(x), int(y))
    )