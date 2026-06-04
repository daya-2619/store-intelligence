from pydantic import BaseModel
from datetime import datetime


class TransactionSchema(BaseModel):

    transaction_id: str

    store_id: str

    timestamp: datetime

    basket_value: float