from fastapi import APIRouter

from app.services.anomaly_service import (
    get_anomalies
)

router = APIRouter()


@router.get(
    "/stores/{store_id}/anomalies"
)
def anomalies(
    store_id: str
):

    return get_anomalies(
        store_id
    )