from app.models import Event
from app.db import SessionLocal
from app.schemas.event import EventSchema
from pydantic import ValidationError

from app.services.session_service import (
    handle_session_events_bulk
)


def ingest_events(events: list):
    print(f"\nINGEST_EVENTS CALLED")

    print(f"Incoming Events: {len(events)}")
    
    if len(events) > 500:
        return {"error": "Batch size exceeds limit of 500 events"}, 400

    db = SessionLocal()

    accepted = 0
    duplicates = 0
    failed = 0
    errors = []

    try:
        parsed_events = []
        for index, event_raw in enumerate(events):
            try:
                parsed_events.append(EventSchema.model_validate(event_raw))
            except ValidationError as e:
                failed += 1
                errors.append({"index": index, "error": str(e)})

        if not parsed_events:
            return {
                "accepted": accepted,
                "duplicates": duplicates,
                "failed": failed,
                "errors": errors
            }

        from sqlalchemy.dialects.postgresql import insert

        event_dicts = []
        valid_events = []

        for event in parsed_events:
            event_dicts.append({
                "event_id": str(event.event_id),
                "store_id": event.store_id,
                "camera_id": event.camera_id,
                "visitor_id": event.visitor_id,
                "event_type": event.event_type,
                "zone_id": event.zone_id,
                "timestamp": event.timestamp,
                "dwell_ms": event.dwell_ms,
                "is_staff": event.is_staff,
                "confidence": event.confidence,
                "event_metadata": event.metadata.model_dump() if event.metadata else {}
            })
            valid_events.append(event)
            accepted += 1
        
        print(f"About to insert {len(event_dicts)} events")
        if event_dicts:
            stmt = insert(Event).values(event_dicts)
            stmt = stmt.on_conflict_do_nothing(index_elements=['event_id'])
            result = db.execute(stmt)
            print("Incoming batch:", len(events))
            print("Valid events:", len(valid_events))
            print("Inserted rows:", result.rowcount)
            handle_session_events_bulk(db, valid_events)
            db.commit()
            
            # P2: Publish event to Redis PubSub for WebSocket broadcasting
            from app.cache import redis_client
            if redis_client:
                for store_id in set([e["store_id"] for e in event_dicts]):
                    redis_client.delete(f"live:{store_id}")
                    redis_client.publish(f"store_update:{store_id}", "updated")
                    
        print("COMMIT SUCCESSFUL")
        return {
            "accepted": accepted,
            "duplicates": duplicates,
            "failed": failed,
            "errors": errors
        }

    finally:

        db.close()