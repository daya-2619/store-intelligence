from fastapi import APIRouter, Response

from app.services.ingestion_service import ingest_events

router = APIRouter()


@router.post("/events/ingest")
def ingest(events: list[dict], response: Response):
    print(
    f"Received {len(events)} events"
)
    result = ingest_events(events)
    if isinstance(result, tuple):
        response.status_code = result[1]
        return result[0]
    return result