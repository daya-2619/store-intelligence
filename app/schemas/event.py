from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import Field
from uuid import UUID, uuid4

class EventMetadata(BaseModel):
    queue_depth: Optional[int] = None
    sku_zone: Optional[str] = None
    session_seq: Optional[int] = None


class EventSchema(BaseModel):

    event_id: UUID = Field(default_factory=uuid4)

    store_id: str

    camera_id: str

    visitor_id: str

    event_type: str

    timestamp: datetime

    zone_id: Optional[str] = None

    dwell_ms: int = 0

    is_staff: bool = False

    confidence: float

    metadata: Optional[EventMetadata] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "store_id": "ST1008",
                    "camera_id": "CAM_1",
                    "visitor_id": "GLOBAL_VISITOR_001",
                    "event_type": "STORE_ENTRY",
                    "timestamp": "2026-06-02T12:00:00Z",
                    "confidence": 0.95
                }
            ]
        }
    }