from app.db import SessionLocal

from app.models import POSTransaction

from app.services.conversion_service import mark_conversion
from app.repositories.transaction_repository import transaction_repository


def ingest_transaction(transaction):

    db = SessionLocal()

    existing = transaction_repository.get_by_transaction_id(db, transaction.transaction_id)

    if existing:

        return {
            "message": "duplicate"
        }

    txn = POSTransaction(

        transaction_id=
        transaction.transaction_id,

        store_id=
        transaction.store_id,

        timestamp=
        transaction.timestamp,

        basket_value_inr=
        transaction.basket_value
    )

    db.add(txn)

    db.commit()

    mark_conversion(transaction)

    db.close()

    return {
        "message":
        "transaction stored"
    }