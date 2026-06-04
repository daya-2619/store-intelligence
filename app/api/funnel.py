from fastapi import APIRouter

from app.services.funnel_service import (
    get_funnel
)

router = APIRouter()


@router.get(
    "/stores/{store_id}/funnel"
)
def funnel(store_id: str):

    return get_funnel(
        store_id
    )