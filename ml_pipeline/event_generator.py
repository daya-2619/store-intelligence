import uuid

from datetime import (
    datetime,
    timezone
)


def base_event(
    track_id,
    store_id,
    camera_id,
    event_type,
    zone=None,
    global_visitor_id=None,
    confidence=0.95
):

    visitor_id = global_visitor_id if global_visitor_id else f"TRACK_{camera_id}_{track_id}"

    return {

        "event_id": str(
            uuid.uuid4()
        ),

        "store_id": store_id,

        "camera_id": camera_id,

        "visitor_id": visitor_id,

        "event_type": event_type,

        "timestamp":
        datetime.now(
            timezone.utc
        ).isoformat(),

        "zone_id": zone,

        "dwell_ms": 0,

        "is_staff": False,

        "confidence": float(confidence),

        "metadata": {

            "queue_depth": 0,

            "sku_zone": zone,

            "session_seq": 1
        }
    }


def create_entry_event(
    track_id,
    store_id,
    camera_id,
    global_visitor_id=None,
    confidence=0.95
):

    return base_event(
        track_id,
        store_id,
        camera_id,
        "ENTRY",
        "ENTRY",
        global_visitor_id
    )


def create_exit_event(
    track_id,
    store_id,
    camera_id,
    global_visitor_id=None,
    confidence=0.95
):

    return base_event(
        track_id,
        store_id,
        camera_id,
        "EXIT",
        "EXIT",
        global_visitor_id,
        confidence=confidence
    )


def create_zone_event(
    track_id,
    zone,
    store_id,
    camera_id,
    global_visitor_id=None,
    confidence=0.95
):

    return base_event(
        track_id,
        store_id,
        camera_id,
        "ZONE_ENTER",
        zone,
        global_visitor_id,
        confidence=confidence
    )

def create_zone_exit_event(
    track_id,
    zone,
    store_id,
    camera_id,
    global_visitor_id=None,
    confidence=0.95
):

    return base_event(
        track_id,
        store_id,
        camera_id,
        "ZONE_EXIT",
        zone,
        global_visitor_id,
        confidence=confidence
    )
    
def create_dwell_event(
    track_id,
    zone,
    store_id,
    camera_id,
    dwell_ms,
    global_visitor_id=None,
    confidence=0.95
):

    event = base_event(
        track_id,
        store_id,
        camera_id,
        "ZONE_DWELL",
        zone,
        global_visitor_id,
        confidence=confidence
    )

    event["dwell_ms"] = dwell_ms

    return event
    
def create_queue_event(
    track_id,
    zone,
    store_id,
    camera_id,
    global_visitor_id=None,
    confidence=0.95
):

    return base_event(
        track_id,
        store_id,
        camera_id,
        "QUEUE_START",
        zone,
        global_visitor_id,
        confidence=confidence
    )
    
def create_purchase_event(
    track_id,
    store_id,
    camera_id
,
    confidence=0.95
):

    return base_event(
        track_id,
        store_id,
        camera_id,
        "PURCHASE",
        "BILLING",
        confidence=confidence
    )
    
def create_queue_end_event(
    track_id,
    zone,
    store_id,
    camera_id,
    global_visitor_id=None,
    confidence=0.95
):

    return base_event(
        track_id,
        store_id,
        camera_id,
        "QUEUE_END",
        zone,
        global_visitor_id,
        confidence=confidence
    )

def create_queue_abandon_event(
    track_id,
    zone,
    store_id,
    camera_id,
    global_visitor_id=None,
    confidence=0.95
):

    return base_event(
        track_id,
        store_id,
        camera_id,
        "BILLING_QUEUE_ABANDON",
        zone,
        global_visitor_id,
        confidence=confidence
    )

def create_reentry_event(
    track_id,
    store_id,
    camera_id,
    global_visitor_id=None,
    confidence=0.95
):

    return base_event(
        track_id,
        store_id,
        camera_id,
        "REENTRY",
        "ENTRY",
        global_visitor_id,
        confidence=confidence
    )