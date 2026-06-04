from fastapi import APIRouter

from app.db import SessionLocal
from app.models import (
    VisitorSession,
    Event,
    POSTransaction
)

from sqlalchemy import func

router = APIRouter()


@router.get("/stores/{store_id}/live/analytics")
def live_analytics(store_id: str):

    db = SessionLocal()

    try:

        active_visitors = (
            db.query(
                VisitorSession
            )
            .filter(
                VisitorSession.store_id == store_id,
                VisitorSession.exit_time == None
            )
            .count()
        )

        avg_dwell = (
            db.query(
                func.avg(
                    Event.dwell_ms
                )
            )
            .filter(
                Event.store_id == store_id,
                Event.event_type == "ZONE_DWELL"
            )
            .scalar()
        )

        orders = (
            db.query(
                func.count(
                    func.distinct(
                        POSTransaction.transaction_id
                    )
                )
            )
            .filter(
                POSTransaction.store_id == store_id
            )
            .scalar()
        )

        revenue = (
            db.query(
                func.sum(
                    POSTransaction.basket_value_inr
                )
            )
            .filter(
                POSTransaction.store_id == store_id
            )
            .scalar()
        )

        total_visitors = (
            db.query(
                VisitorSession
            )
            .filter(
                VisitorSession.store_id == store_id
            )
            .count()
        )

        converted = (
            db.query(
                VisitorSession
            )
            .filter(
                VisitorSession.store_id == store_id,
                VisitorSession.converted == True
            )
            .count()
        )

        conversion_rate = 0

        if total_visitors:

            conversion_rate = round(
                (
                    converted
                    / total_visitors
                ) * 100,
                2
            )

        return {

            "active_visitors":
            active_visitors,

            "queue_size":
            0,

            "avg_dwell_time":
            round(
                avg_dwell or 0,
                2
            ),

            "conversion_rate":
            conversion_rate,

            "revenue":
            round(
                revenue or 0,
                2
            ),

            "orders":
            orders or 0
        }

    finally:

        db.close()