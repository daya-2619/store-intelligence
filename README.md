# Store Intelligence

Store Intelligence is an event-driven computer vision platform designed to turn physical retail stores into highly measurable, real-time analytics dashboards.

## Features
- **Cross-Camera Re-ID**: Tracks individuals across multiple cameras using OSNet to prevent double counting.
- **Event-Driven Architecture**: YOLOv8 + ByteTrack detect physical movements and push events directly into RabbitMQ.
- **Real-Time Analytics**: FastAPI backend calculates metrics, anomaly detection, queue abandonment, and funnel conversions.
- **WebSockets & Redis**: Aggregations are heavily cached using Redis. Live camera statistics stream to the Next.js frontend via WebSockets instantly.
- **Spatial Heatmaps**: Generates visual store heatmaps dynamically from raw Cartesian point data.

## Requirements
- Docker & Docker Compose
- Python 3.10+
- Node.js 18+

## Quickstart (Docker)

```bash
# 1. Build and boot all infrastructure
docker-compose up -d --build

# 2. Run the mock CV pipeline
python scripts/simulate_camera_feeds.py
```

Visit `http://localhost:3000` to access the Live Dashboard!
