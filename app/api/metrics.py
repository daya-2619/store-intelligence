from fastapi import APIRouter, Depends, HTTPException

from app.services.metrics_service import (
    get_store_metrics
)
from app.api.auth import get_current_user

router = APIRouter()


@router.get(
    "/stores/{store_id}/metrics"
)
def metrics(store_id: str, user: dict = Depends(get_current_user)):
    # Optional RBAC check
    if user["stores"] != ["*"] and store_id not in user["stores"]:
        raise HTTPException(status_code=403, detail="Not authorized for this store")


    return get_store_metrics(
        store_id
    )