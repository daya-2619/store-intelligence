from sqlalchemy import func

from app.db import SessionLocal

from app.models import (
    VisitorSession,
    POSTransaction,
    BillingVisit,
    Event
)


def get_store_health(store_id):

    db = SessionLocal()

    try:

        # -------------------------
        # Visitors
        # -------------------------

        visitors = (

            db.query(
                VisitorSession
            )

            .filter(
                VisitorSession.store_id == store_id,
                VisitorSession.is_staff == False
            )

            .count()
        )

        # -------------------------
        # Converted Visitors
        # -------------------------

        converted = (

            db.query(
                VisitorSession
            )

            .filter(
                VisitorSession.store_id == store_id,
                VisitorSession.is_staff == False,
                VisitorSession.converted == True
            )

            .count()
        )

        conversion_rate = 0

        if visitors:

            conversion_rate = (
                converted
                / visitors
            ) * 100

        # -------------------------
        # Revenue
        # -------------------------

        revenue = (

            db.query(
                func.sum(
                    POSTransaction.basket_value_inr
                )
            )

            .filter(
                POSTransaction.store_id
                == store_id
            )

            .scalar()

        ) or 0

        # -------------------------
        # Average Dwell
        # -------------------------

        avg_dwell = (

            db.query(
                func.avg(
                    Event.dwell_ms
                )
            )

            .filter(
                Event.store_id == store_id,
                Event.event_type == "ZONE_DWELL",
                Event.is_staff == False
            )

            .scalar()

        ) or 0

        # -------------------------
        # Queue Size
        # -------------------------

        queue_events = (

            db.query(
                Event
            )

            .filter(
                Event.store_id == store_id,
                Event.event_type == "BILLING_QUEUE_JOIN",
                Event.is_staff == False
            )

            .count()
        )

        # -------------------------
        # Health Score
        # -------------------------

        health = 100

        # Conversion Impact
        if conversion_rate < 15:
            health -= 25

        elif conversion_rate < 30:
            health -= 10

        # Queue Impact
        if queue_events > 10:
            health -= 20

        elif queue_events > 5:
            health -= 10

        # Dwell Impact
        if avg_dwell > 60000:
            health -= 15

        elif avg_dwell > 30000:
            health -= 8

        # Revenue Bonus
        if revenue > 50000:
            health += 5

        # Empty Store Impact
        active_visitors = (
            db.query(VisitorSession)
            .filter(
                VisitorSession.store_id == store_id,
                VisitorSession.exit_time == None,
                VisitorSession.is_staff == False
            )
            .count()
        )

        if active_visitors == 0:
            health -= 50
        elif active_visitors < 5:
            health -= 20

        health = max(
            0,
            min(
                100,
                round(health, 2)
            )
        )

        if health >= 80:
            status = "EXCELLENT"

        elif health >= 60:
            status = "GOOD"

        elif health >= 40:
            status = "WARNING"

        else:
            status = "CRITICAL"
            
        # STALE_FEED check
        from datetime import datetime, timedelta
        last_event = db.query(Event.timestamp).filter(Event.store_id == store_id).order_by(Event.timestamp.desc()).first()
        if last_event and (datetime.utcnow() - last_event[0].replace(tzinfo=None)) > timedelta(minutes=10):
            status = "STALE_FEED"

        return {

            "store_id": store_id,

            "health_score": health,

            "status": status,

            "conversion_rate": round(
                conversion_rate,
                2
            ),

            "avg_dwell_time": round(
                avg_dwell,
                2
            ),

            "queue_events": queue_events,

            "revenue": round(
                revenue,
                2
            )
        }

    finally:

        db.close()