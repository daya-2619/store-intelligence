from typing import Optional, List
from sqlalchemy.orm import Session
from app.models import POSTransaction
from app.repositories.base import BaseRepository

class TransactionRepository(BaseRepository[POSTransaction]):
    def __init__(self):
        super().__init__(POSTransaction)

    def get_by_transaction_id(self, db: Session, transaction_id: str) -> Optional[POSTransaction]:
        return db.query(self.model).filter(self.model.transaction_id == transaction_id).first()

    def get_by_store(self, db: Session, store_id: str) -> List[POSTransaction]:
        return db.query(self.model).filter(self.model.store_id == store_id).all()

    def get_in_time_range(self, db: Session, store_ids: List[str], min_time, max_time) -> List[POSTransaction]:
        return db.query(self.model).filter(
            self.model.store_id.in_(store_ids),
            self.model.timestamp >= min_time,
            self.model.timestamp <= max_time
        ).all()

transaction_repository = TransactionRepository()
