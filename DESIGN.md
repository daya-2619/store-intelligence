# Architecture Design

## 1. Computer Vision Pipeline (The Edge)
Raw video feeds are processed locally using `YOLOv8` for bounding box detection and `ByteTrack` for frame-by-frame persistent object tracking. As a person moves through predefined `zones`, an Event Generator constructs telemetry payloads.

To ensure individuals aren't double-counted across different camera feeds, we implemented a Re-Identification (Re-ID) layer utilizing `OSNet`. Every tracked crop generates a 512-dimensional embedding, matched against a global memory bank via Cosine Similarity, assigning a unified `GLOBAL_VISITOR_ID`.

## 2. Event-Driven Ingestion (The Message Broker)
Telemetry is passed from the Edge into a centralized `RabbitMQ` message broker. A background Python daemon (`event_consumer.py`) subscribes to the `store_events` queue, batches payloads into arrays of 500, and performs bulk `UPSERT` operations directly into PostgreSQL.

## 3. The Backend API & Caching Layer
The backend is a `FastAPI` service built around SQLAlchemy Core. Complex calculations (e.g., POS summaries, historical funnel analysis) are aggressively cached using `Redis` with a 10-second TTL to prevent database strain.

## 4. Real-Time WebSockets
For mission-critical live metrics (active visitor counts, queue lengths, live camera health), the backend opens a `WebSocket` connection with the Next.js frontend. Data is parsed and pushed out to connected clients instantly.

## 5. AI-Assisted Decisions
Throughout the development of Store Intelligence, AI tools were utilized to accelerate engineering and validate architectural choices. Key areas of AI assistance included:
- **Architecture Validation**: Used AI to compare message brokers (RabbitMQ vs Kafka) for edge telemetry, confirming RabbitMQ's suitability for high-speed ephemeral event buffering.
- **Query Optimization**: AI assisted in crafting the highly optimized SQLAlchemy Core `UPSERT` statements to handle 500 events per second without ORM overhead.
- **Frontend Scaffolding**: Leveraged AI for rapid scaffolding of the Next.js real-time dashboard and WebSocket client logic.
- **Documentation**: AI was used to draft and structure the README, DESIGN, and CHOICES documentation for clarity and completeness.
