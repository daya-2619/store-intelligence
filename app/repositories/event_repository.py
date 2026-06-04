from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import Event
from app.repositories.base import BaseRepository

class EventRepository(BaseRepository[Event]):
    def __init__(self):
        super().__init__(Event)

    def get_by_event_id(self, db: Session, event_id: str) -> Optional[Event]:
        return db.query(self.model).filter(self.model.event_id == event_id).first()

    def get_by_store(self, db: Session, store_id: str, limit: int = 100) -> List[Event]:
        return db.query(self.model).filter(self.model.store_id == store_id).order_by(self.model.timestamp.desc()).limit(limit).all()

    def count_events(self, db: Session, store_id: str, event_type: str) -> int:
        return db.query(self.model.visitor_id).filter(
            self.model.store_id == store_id,
            self.model.event_type == event_type,
            self.model.is_staff == False
        ).distinct().count()

    def count_grouped_events(self, db: Session, store_id: str) -> dict:
        from sqlalchemy import func
        results = db.query(
            self.model.event_type,
            func.count(func.distinct(self.model.visitor_id))
        ).filter(
            self.model.store_id == store_id,
            self.model.is_staff == False
        ).group_by(
            self.model.event_type
        ).all()
        return dict(results)

    def get_avg_dwell(self, db: Session, store_id: str):
        from sqlalchemy import func
        return db.query(func.avg(self.model.dwell_ms)).filter(
            self.model.store_id == store_id,
            self.model.event_type == "ZONE_DWELL",
            self.model.is_staff == False
        ).scalar()

    def count_recent_events(self, db: Session, store_id: str, event_type: str, min_time):
        return db.query(self.model).filter(
            self.model.store_id == store_id,
            self.model.event_type == event_type,
            self.model.timestamp >= min_time,
            self.model.is_staff == False
        ).count()

event_repository = EventRepository()
