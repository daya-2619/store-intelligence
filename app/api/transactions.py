from fastapi import APIRouter

from app.schemas.transaction import (
    TransactionSchema
)

from app.services.transaction_service import (
    ingest_transaction
)

router = APIRouter()


@router.post("/transactions")

def create_transaction(
    transaction: TransactionSchema
):

    return ingest_transaction(
        transaction
    )