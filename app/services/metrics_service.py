from sqlalchemy import func

from app.db import SessionLocal
from datetime import datetime, timedelta, timezone

from app.models import (
    VisitorSession,
    Event,
    BillingVisit
)
from app.repositories.session_repository import session_repository
from app.repositories.event_repository import event_repository


def get_store_metrics(store_id):

    db = SessionLocal()

    try:

        visitors = session_repository.count_by_store(db, store_id)

        converted = session_repository.count_converted_by_store(db, store_id)

        active_visitors = session_repository.count_active_by_store(db, store_id)

        avg_dwell = event_repository.get_avg_dwell(db, store_id)
        recent = (
            datetime.now(timezone.utc) - timedelta(minutes=5)
        )
        queue_size = event_repository.count_recent_events(db, store_id, "BILLING_QUEUE_JOIN", recent)

        queue_joins = event_repository.count_events(db, store_id, "BILLING_QUEUE_JOIN")

        queue_abandons = event_repository.count_events(db, store_id, "BILLING_QUEUE_ABANDON")

        abandonment_rate = 0
        if queue_joins:
            abandonment_rate = (queue_abandons / queue_joins) * 100

        conversion_rate = 0

        if visitors:

            conversion_rate = (
                converted
                / visitors
            ) * 100

        return {

            "unique_visitors":
                visitors,

            "active_visitors":
                active_visitors,

            "converted_visitors":
                converted,

            "avg_dwell_time":
                round(
                    avg_dwell or 0,
                    2
                ),

            "queue_size":
                queue_size,

            "abandonment_rate":
                round(
                    abandonment_rate,
                    2
                ),

            "conversion_rate":
                round(
                    conversion_rate,
                    2
                )
        }

    finally:

        db.close()