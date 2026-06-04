from typing import Optional, List
from sqlalchemy.orm import Session
from app.models import VisitorSession
from app.repositories.base import BaseRepository

class SessionRepository(BaseRepository[VisitorSession]):
    def __init__(self):
        super().__init__(VisitorSession)

    def get_by_visitor(self, db: Session, visitor_id: str) -> Optional[VisitorSession]:
        return db.query(self.model).filter(self.model.visitor_id == visitor_id).first()

    def get_by_ids(self, db: Session, visitor_ids: List[str], store_ids: List[str]) -> List[VisitorSession]:
        return db.query(self.model).filter(
            self.model.visitor_id.in_(visitor_ids),
            self.model.store_id.in_(store_ids)
        ).all()

    def count_by_store(self, db: Session, store_id: str) -> int:
        return db.query(self.model).filter(self.model.store_id == store_id, self.model.is_staff == False).count()

    def count_converted_by_store(self, db: Session, store_id: str) -> int:
        return db.query(self.model).filter(self.model.store_id == store_id, self.model.converted == True, self.model.is_staff == False).count()

    def count_active_by_store(self, db: Session, store_id: str) -> int:
        return db.query(self.model).filter(self.model.store_id == store_id, self.model.exit_time == None, self.model.is_staff == False).count()

session_repository = SessionRepository()
