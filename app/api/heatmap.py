from fastapi import APIRouter

from app.services.heatmap_service import (
    get_heatmap
)

router = APIRouter()


@router.get(
    "/stores/{store_id}/heatmap"
)
def heatmap(store_id: str):

    return get_heatmap(store_id)