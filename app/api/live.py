from fastapi import APIRouter
from app.db import SessionLocal
from app.models import VisitorSession, Event, Camera
from app.services.anomaly_service import get_anomalies
from datetime import datetime, timedelta

from app.cache import get_cache, set_cache

router = APIRouter()

@router.get("/stores/{store_id}/live")
def get_live_dashboard(store_id: str):
    cache_key = f"live:{store_id}"
    cached = get_cache(cache_key)
    if cached:
        return cached

    db = SessionLocal()
    try:
        active_visitors = db.query(VisitorSession).filter(
            VisitorSession.store_id == store_id,
            VisitorSession.exit_time == None,
            VisitorSession.is_staff == False
        ).count()

        # To get queue size reliably without a complex state machine query, 
        # we can look for recent BILLING events, or just a simple aggregate.
        from datetime import timezone
        recent_time = datetime.now(timezone.utc) - timedelta(minutes=15)
        queue_size = db.query(Event.visitor_id).filter(
            Event.store_id == store_id,
            Event.event_type == "BILLING_QUEUE_JOIN",
            Event.timestamp >= recent_time,
            Event.is_staff == False
        ).distinct().count()

        cameras = db.query(Camera).filter(Camera.store_id == store_id).all()
        camera_status = []
        for cam in cameras:
            cam_id_db = cam.camera_id
            
            # Simple mock/heuristic for camera specific active counts
            cam_visitors = db.query(Event.visitor_id).filter(
                Event.store_id == store_id,
                Event.camera_id == cam_id_db,
                Event.timestamp >= recent_time,
                Event.is_staff == False
            ).distinct().count()

            cam_queue_size = db.query(Event.visitor_id).filter(
                Event.store_id == store_id,
                Event.camera_id == cam_id_db,
                Event.event_type == "BILLING_QUEUE_JOIN",
                Event.timestamp >= recent_time,
                Event.is_staff == False
            ).distinct().count()

            camera_status.append({
                "camera_id": cam_id_db,
                "status": cam.status,
                "active_visitors": cam_visitors,
                "queue_size": cam_queue_size,
                "stream_url": cam.stream_url
            })

        anomalies_data = get_anomalies(store_id)
        
        response = {
            "active_visitors": active_visitors,
            "queue_size": queue_size,
            "alerts": anomalies_data.get("anomalies", []),
            "camera_status": camera_status
        }
        
        set_cache(cache_key, response, ttl=2)
        return response
    finally:
        db.close()
