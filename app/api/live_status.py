from fastapi import APIRouter

from ml_pipeline.state_manager import StoreStateManager

router = APIRouter()


from app.services.live_metrics_service import live_metrics_service

@router.get(
    "/stores/{store_id}/live/status"
)
def live_status(store_id: str):
    state = StoreStateManager(store_id)
    return {

        "active_visitors":
        len(state.active_tracks)
    }

@router.get("/stores/{store_id}/live-cctv")
def get_live_cctv(store_id: str):
    return live_metrics_service.get_live_cctv_feeds(store_id)

@router.get("/stores/{store_id}/alerts")
def get_alerts(store_id: str):
    return live_metrics_service.get_realtime_alerts(store_id)