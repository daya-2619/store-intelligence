ZONES = {

    "ENTRY": (
        0,
        300,
        300,
        1000
    ),

    "BOTTOM_SHELF": (
        300,
        650,
        1600,
        1000
    ),

    "TOP_SHELF": (
        300,
        0,
        1600,
        250
    ),

    "CENTER_ISLAND": (
        300,
        250,
        1200,
        650
    ),

    "BILLING": (
        1250,
        150,
        1700,
        650
    )
}


def get_zone(x, y):

    for zone_name, (
        x1,
        y1,
        x2,
        y2
    ) in ZONES.items():

        if (
            x1 <= x <= x2
            and
            y1 <= y <= y2
        ):

            return zone_name

    return None