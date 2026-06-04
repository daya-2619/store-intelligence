from fastapi import APIRouter

from app.services.health_service import (
    get_store_health
)

router = APIRouter()


@router.get(
    "/stores/{store_id}/health"
)
def health(
    store_id: str
):
    from app.cache import get_cache, set_cache
    cache_key = f"health:{store_id}"
    cached = get_cache(cache_key)
    if cached:
        return cached
        
    res = get_store_health(store_id)
    set_cache(cache_key, res, ttl=10)
    return res