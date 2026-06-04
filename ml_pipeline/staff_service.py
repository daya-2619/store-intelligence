def detect_staff(
    visitor_id,
    state
):
    state.staff_candidates[
        visitor_id
    ] = (
        state.staff_candidates.get(
            visitor_id,
            0
        ) + 1
    )

    return (
        state.staff_candidates[
            visitor_id
        ] > 500
    )