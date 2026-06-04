from typing import Optional, List
from sqlalchemy.orm import Session
from app.models import BillingVisit
from app.repositories.base import BaseRepository

class BillingRepository(BaseRepository[BillingVisit]):
    def __init__(self):
        super().__init__(BillingVisit)

    def get_by_visitor(self, db: Session, visitor_id: str) -> Optional[BillingVisit]:
        return db.query(self.model).filter(self.model.visitor_id == visitor_id).first()

    def get_by_store(self, db: Session, store_id: str) -> List[BillingVisit]:
        return db.query(self.model).filter(self.model.store_id == store_id).all()

    def get_by_ids(self, db: Session, visitor_ids: List[str]) -> List[BillingVisit]:
        return db.query(self.model).filter(self.model.visitor_id.in_(visitor_ids)).all()

    def count_billing_visitors(self, db: Session, store_id: str) -> int:
        from app.models import VisitorSession
        return db.query(self.model.visitor_id).join(VisitorSession, VisitorSession.visitor_id == self.model.visitor_id).filter(
            self.model.store_id == store_id, VisitorSession.is_staff == False
        ).distinct().count()

billing_repository = BillingRepository()
