# API Documentation

## REST Endpoints

### `GET /pos/summary`
Returns aggregated Point of Sale metrics (Total Revenue, Total Orders, Average Order Value). Cached via Redis.

### `GET /stores/{store_id}/metrics`
Returns core conversion metrics (Total Visitors, Converted Customers, Avg Dwell Time, Avg Queue Time). Automatically excludes Staff.

### `GET /stores/{store_id}/funnel`
Returns the operational funnel tracking (Entered, Approached Billing, Abandoned Queue, Completed Purchase).

### `GET /stores/{store_id}/visual-heatmap`
Returns the URL to the latest dynamically generated spatial heatmap PNG for the store.

### `GET /stores/{store_id}/anomalies`
Evaluates and returns real-time alerts (e.g., HIGH_QUEUE_ABANDONMENT, QUEUE_SPIKE).

### `GET /stores/{store_id}/health`
Returns the operational health score (0-100) based on camera uptime and data staleness.

## WebSocket Endpoints

### `WS /websocket/live/{store_id}`
Establishes a persistent bi-directional connection. The server pushes real-time JSON payloads containing `live` (active visitors, queue size, per-camera status) and `metrics` (anomalies) directly to the client every 2 seconds.
