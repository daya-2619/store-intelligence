# Technical Choices & Rationale

### 1. OSNet over FastReID/BoT
We chose **OSNet** (Omni-Scale Network) for our cross-camera tracking. While FastReID boasts higher benchmarks on modern datasets, OSNet provides an incredibly lightweight 512-dimensional feature vector while retaining extremely high accuracy across varied resolutions. This is vital for running multi-camera inference on constrained edge hardware without needing specialized massive GPU clusters.

### 2. RabbitMQ over Kafka
While Kafka excels at massive, permanent event streaming and replayability, our system inherently treats physical telemetry as ephemeral until it hits the database. **RabbitMQ** offers lower latency for real-time routing and simpler architectural deployment, perfectly matching our need to simply buffer high-speed bursts of tracking data (preventing DB connection exhaustion) before bulk insertion.

### 3. Schema Design: PostgreSQL Bulk Upserts over ORM
We bypassed SQLAlchemy's standard ORM `db.add()` for event ingestion, opting instead for `insert().on_conflict_do_nothing()` against a heavily normalized, index-optimized schema. Handling 500 events per second via an ORM triggers N+1 lookup queries resulting in immediate CPU thrashing. Raw SQLAlchemy Core UPSERTs condensed 500 queries into a single atomic transaction.

### 4. API Architecture: Redis Caching
Real-time dashboards often suffer from "F5 Attacks", where multiple users repeatedly query the same complex aggregations. Our API Architecture wraps the `pos_summary` and `live` endpoints in a simple Redis cache, completely isolating the database from read-heavy dashboard spikes.
