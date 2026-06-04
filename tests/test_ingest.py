import pytest
from app.services.ingestion_service import ingest_events
from app.db import SessionLocal
from app.models import Event

def test_bulk_ingestion():
    import uuid
    # Setup dummy events
    events = [
        {"event_id": str(uuid.uuid4()), "visitor_id": "T1", "camera_id": "C1", "store_id": "ST1008", "event_type": "ZONE_ENTER", "zone_id": "ENTRANCE", "timestamp": "2024-01-01T10:00:00Z", "confidence": 0.9},
        {"event_id": str(uuid.uuid4()), "visitor_id": "T2", "camera_id": "C1", "store_id": "ST1008", "event_type": "ZONE_ENTER", "zone_id": "ENTRANCE", "timestamp": "2024-01-01T10:00:05Z", "confidence": 0.95}
    ]
    
    res = ingest_events(events)
    assert res["failed"] == 0
    assert res["accepted"] == 2
    
    import app.db
    db = app.db.SessionLocal()
    count = db.query(Event).filter(Event.visitor_id.in_(["T1", "T2"])).count()
    assert count >= 2
    db.close()
