from datetime import datetime, timezone
import uuid

class EventFactory:
    @staticmethod
    def base_event(track_id: str, store_id: str, camera_id: str, event_type: str, zone: str = None, confidence: float = 0.95) -> dict:
        visitor_id = f"TRACK_{camera_id}_{track_id}"
        return {
            "event_id": str(uuid.uuid4()),
            "store_id": store_id,
            "camera_id": camera_id,
            "visitor_id": visitor_id,
            "event_type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
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

    @staticmethod
    def create_entry_event(track_id: str, store_id: str, camera_id: str, is_staff: bool = False) -> dict:
        event = EventFactory.base_event(track_id, store_id, camera_id, "ENTRY", "ENTRY", confidence=confidence)
        event["is_staff"] = is_staff
        return event

    @staticmethod
    def create_exit_event(track_id: str, store_id: str, camera_id: str) -> dict:
        return EventFactory.base_event(track_id, store_id, camera_id, "EXIT", "EXIT", confidence=confidence)

    @staticmethod
    def create_zone_event(track_id: str, zone: str, store_id: str, camera_id: str, is_staff: bool = False) -> dict:
        event = EventFactory.base_event(track_id, store_id, camera_id, "ZONE_ENTER", zone, confidence=confidence)
        event["is_staff"] = is_staff
        return event

    @staticmethod
    def create_dwell_event(track_id: str, zone: str, store_id: str, camera_id: str, dwell_ms: int, is_staff: bool = False) -> dict:
        event = EventFactory.base_event(track_id, store_id, camera_id, "ZONE_DWELL", zone, confidence=confidence)
        event["dwell_ms"] = dwell_ms
        event["is_staff"] = is_staff
        return event

    @staticmethod
    def create_queue_event(track_id: str, zone: str, store_id: str, camera_id: str, is_staff: bool = False) -> dict:
        event = EventFactory.base_event(track_id, store_id, camera_id, "BILLING_QUEUE_JOIN", zone, confidence=confidence)
        event["is_staff"] = is_staff
        return event

    @staticmethod
    def create_queue_end_event(track_id: str, zone: str, store_id: str, camera_id: str) -> dict:
        return EventFactory.base_event(track_id, store_id, camera_id, "BILLING_QUEUE_ABANDON", zone, confidence=confidence)

