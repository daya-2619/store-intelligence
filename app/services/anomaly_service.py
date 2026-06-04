from sqlalchemy import func

from app.db import SessionLocal
from app.models import (
    Event,
    VisitorSession
)


def get_anomalies(store_id):

    db = SessionLocal()

    anomalies = []

    try:

        # =====================================
        # Queue Spike Detection
        # =====================================

        max_queue = 0

        events = (

            db.query(Event)

            .filter(
                Event.store_id == store_id,
                Event.is_staff == False
            )

            .all()
        )

        for event in events:

            metadata = (
                event.event_metadata
                or {}
            )

            queue_depth = (
                metadata.get(
                    "queue_depth",
                    0
                )
            )

            try:

                max_queue = max(
                    max_queue,
                    int(queue_depth or 0)
                )

            except (
                ValueError,
                TypeError
            ):
                pass

        if max_queue > 5:
            anomalies.append({
                "type": "QUEUE_SPIKE",
                "severity": "CRITICAL",
                "value": max_queue,
                "suggested_action": "Deploy additional staff to billing counters immediately."
            })

        # =====================================
        # Queue Congestion
        # =====================================

        queue_events = (

            db.query(Event)

            .filter(
                Event.store_id == store_id,
                Event.event_type == "BILLING_QUEUE_JOIN",
                Event.is_staff == False
            )

            .count()
        )

        if queue_events > 10:
            anomalies.append({
                "type": "QUEUE_CONGESTION",
                "severity": "WARN",
                "queue_events": queue_events,
                "suggested_action": "Monitor billing area closely. Prepare to open new lane."
            })
            
        abandonments = (
            db.query(Event)
            .filter(
                Event.store_id == store_id,
                Event.event_type == "BILLING_QUEUE_ABANDON",
                Event.is_staff == False
            )
            .count()
        )
        
        if abandonments > 2:
            anomalies.append({
                "type": "HIGH_QUEUE_ABANDONMENT",
                "severity": "CRITICAL",
                "abandonments": abandonments,
                "suggested_action": "Open a new billing lane immediately. Customers are leaving without purchasing."
            })

        # =====================================
        # Conversion Drop
        # =====================================

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

        converted = (

            db.query(
                VisitorSession
            )

            .filter(
                VisitorSession.store_id == store_id,
                VisitorSession.converted == True,
                VisitorSession.is_staff == False
            )

            .count()
        )

        conversion_rate = 0

        if visitors:

            conversion_rate = (
                converted
                / visitors
            ) * 100

        if (
            visitors >= 5
            and conversion_rate < 10
        ):
            anomalies.append({
                "type": "CONVERSION_DROP",
                "severity": "CRITICAL",
                "conversion_rate": round(conversion_rate, 2),
                "suggested_action": "Investigate immediately. High traffic but extremely low conversion."
            })

        # =====================================
        # Long Dwell Detection
        # =====================================

        long_dwell = (

            db.query(Event)

            .filter(
                Event.store_id == store_id,
                Event.event_type == "ZONE_DWELL",
                Event.dwell_ms > 30000,
                Event.is_staff == False
            )

            .count()
        )

        if long_dwell > 0:
            anomalies.append({
                "type": "LONG_DWELL",
                "severity": "WARN",
                "count": long_dwell,
                "suggested_action": "Assign floor staff to assist dwelling customers."
            })

        # =====================================
        # Dead Zones
        # =====================================

        retail_zones = [

            "CENTER_ISLAND",
            "BOTTOM_SHELF",
            "BILLING"
        ]

        from datetime import datetime, timedelta, timezone
        thirty_mins_ago = datetime.now(timezone.utc) - timedelta(minutes=30)
        
        for zone in retail_zones:
            visits = (
                db.query(Event)
                .filter(
                    Event.store_id == store_id,
                    Event.event_type == "ZONE_ENTER",
                    Event.zone_id == zone,
                    Event.timestamp >= thirty_mins_ago,
                    Event.is_staff == False
                )
                .count()
            )

            if visits == 0:
                anomalies.append({
                    "type": "DEAD_ZONE",
                    "zone": zone,
                    "severity": "INFO",
                    "suggested_action": f"Check {zone} for obstructions, lighting issues, or unappealing displays."
                })

        # =====================================
        # Low Activity Warning
        # =====================================

        total_events = (

            db.query(Event)

            .filter(
                Event.store_id == store_id,
                Event.is_staff == False
            )

            .count()
        )

        if total_events < 20:
            anomalies.append({
                "type": "LOW_ACTIVITY",
                "severity": "INFO",
                "events": total_events,
                "suggested_action": "Verify if the store is open and camera feeds are working properly."
            })

        return {

            "store_id":
                store_id,

            "anomalies":
                anomalies
        }

    finally:

        db.close()