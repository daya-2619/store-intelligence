from sqlalchemy import func

from app.db import SessionLocal
from app.models import Event


def get_heatmap(store_id):

    db = SessionLocal()

    try:

        # Get all zones visited
        zones = (

            db.query(
                Event.zone_id
            )

            .filter(
                Event.store_id == store_id,
                Event.zone_id.isnot(None),
                Event.is_staff == False
            )

            .distinct()

            .all()
        )

        response = {}

        total_visits = 0

        for (zone,) in zones:

            # Zone Visits
            visits = (

                db.query(
                    Event
                )

                .filter(
                    Event.store_id == store_id,
                    Event.event_type == "ZONE_ENTER",
                    Event.zone_id == zone,
                    Event.is_staff == False
                )

                .count()
            )

            # Average Dwell Time
            avg_dwell = (

                db.query(
                    func.avg(
                        Event.dwell_ms
                    )
                )

                .filter(
                    Event.store_id == store_id,
                    Event.event_type == "ZONE_DWELL",
                    Event.zone_id == zone,
                    Event.is_staff == False
                )

                .scalar()
            )

            # Queue Events
            queue_count = (

                db.query(
                    Event
                )

                .filter(
                    Event.store_id == store_id,
                    Event.event_type == "BILLING_QUEUE_JOIN",
                    Event.zone_id == zone,
                    Event.is_staff == False
                )

                .count()
            )

            total_visits += visits

            response[zone] = {

                "visits": visits,

                "avg_dwell": round(
                    float(avg_dwell) if avg_dwell is not None else 0.0,
                    2
                ),

                "queue_events": queue_count
            }

        from app.models import VisitorSession
        sessions = db.query(VisitorSession).filter(VisitorSession.store_id == store_id, VisitorSession.is_staff == False).count()

        response["data_confidence"] = "HIGH" if sessions >= 20 else "LOW"
        response["total_zone_visits"] = total_visits

        # Normalize metrics 0-100
        max_visits = max([data["visits"] for zone, data in response.items() if zone not in ["data_confidence", "total_zone_visits"]] + [1])
        max_dwell = max([data["avg_dwell"] for zone, data in response.items() if zone not in ["data_confidence", "total_zone_visits"]] + [1])

        for zone in response:
            if zone not in ["data_confidence", "total_zone_visits"]:
                visits_score = (response[zone]["visits"] / max_visits) * 100
                dwell_score = (response[zone]["avg_dwell"] / max_dwell) * 100
                response[zone]["normalized_score"] = round((visits_score * 0.5) + (dwell_score * 0.5), 2)

        return response

    finally:
        db.close()