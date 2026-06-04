from fastapi import APIRouter

from app.services.pos_summary_service import (
    get_pos_summary
)

router = APIRouter()


@router.get("/stores/{store_id}/pos/summary")
def pos_summary(store_id: str):
    from app.cache import get_cache, set_cache
    cache_key = f"pos:summary:{store_id}"
    cached = get_cache(cache_key)
    if cached:
        return cached
    
    res = get_pos_summary(store_id)
    set_cache(cache_key, res, ttl=10)
    return res