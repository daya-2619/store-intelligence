from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import logging
from pythonjsonlogger import jsonlogger

logger = logging.getLogger()
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s')
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

from app.api.ingest import router as ingest_router
from app.api.metrics import router as metrics_router
from app.api.transactions import router as transaction_router
from app.api.funnel import router as funnel_router
from app.api.heatmap import router as heatmap_router
from app.api.pos import router as pos_router
from app.api.pos_summary import router as pos_summary_router
from app.api.anomalies import router as anomalies_router
from app.api.live_heatmap import router as live_heatmap_router
from app.api.live_status import router as live_status_router
from app.api.live_analytics import router as live_analytics_router
from app.api.health import router as health_router
from app.api.visual_heatmap import router as visual_heatmap_router
from app.api.live import router as live_router
from app.api.websocket import router as websocket_router
from app.api.stores import router as stores_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.middleware.rate_limiter import RateLimiterMiddleware
app.add_middleware(RateLimiterMiddleware, max_requests=100, window_seconds=60)

# Ensure heatmaps directory exists and mount it
os.makedirs(os.path.join(os.path.dirname(__file__), '..', 'heatmaps'), exist_ok=True)
app.mount("/heatmaps", StaticFiles(directory=os.path.join(os.path.dirname(__file__), '..', 'heatmaps')), name="heatmaps")

# Mount CCTV Footage
cctv_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'CCTV Footage')
if os.path.exists(cctv_dir):
    app.mount("/cctv", StaticFiles(directory=cctv_dir), name="cctv")

from app.api.auth import router as auth_router

app.include_router(auth_router)
app.include_router(ingest_router)
app.include_router(metrics_router)
app.include_router(transaction_router)
app.include_router(funnel_router)
app.include_router(heatmap_router)
app.include_router(pos_router)
app.include_router(pos_summary_router)
app.include_router(anomalies_router)
app.include_router(live_heatmap_router)
app.include_router(live_status_router)
app.include_router(live_analytics_router)
app.include_router(health_router)
app.include_router(visual_heatmap_router)
app.include_router(live_router)
app.include_router(websocket_router)
app.include_router(stores_router)

@app.get("/")
def root():
    return {
        "message": "Store Intelligence API"
    }

@app.get("/health")
def health():
    from app.db import SessionLocal
    from sqlalchemy import text
    from app.cache import redis_client
    import pika
    import os
    from datetime import datetime, timezone
    
    status = {
        "status": "healthy",
        "database": "unhealthy",
        "redis": "unhealthy",
        "rabbitmq": "unhealthy",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
        status["database"] = "healthy"
    except Exception:
        status["status"] = "unhealthy"
    finally:
        db.close()
        
    try:
        if redis_client and redis_client.ping():
            status["redis"] = "healthy"
        else:
            status["status"] = "unhealthy"
    except Exception:
        status["status"] = "unhealthy"
        
    try:
        rabbitmq_host = os.getenv("RABBITMQ_HOST", "localhost")
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, heartbeat=0))
        if connection.is_open:
            status["rabbitmq"] = "healthy"
            connection.close()
        else:
            status["status"] = "unhealthy"
    except Exception:
        status["status"] = "unhealthy"
        
    return status