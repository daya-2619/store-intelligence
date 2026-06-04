from app.db import SessionLocal

from app.repositories.session_repository import session_repository
from app.repositories.event_repository import event_repository
from app.repositories.billing_repository import billing_repository


def get_funnel(store_id):

    db = SessionLocal()

    try:

        # -------------------------
        # Entry Visitors
        # -------------------------

        entries = session_repository.count_by_store(db, store_id)

        # -------------------------
        # Grouped Events
        # -------------------------

        event_counts = event_repository.count_grouped_events(db, store_id)

        zone_visits = event_counts.get("ZONE_ENTER", 0)
        dwell_visitors = event_counts.get("ZONE_DWELL", 0)
        queued_visitors = event_counts.get("BILLING_QUEUE_JOIN", 0)
        abandoned_queue_count = event_counts.get("BILLING_QUEUE_ABANDON", 0)
        exit_count = event_counts.get("EXIT", 0)

        # -------------------------
        # Billing & Purchase Visitors
        # -------------------------

        billing = billing_repository.count_billing_visitors(db, store_id)
        purchases = session_repository.count_converted_by_store(db, store_id)

        return {

            "entry": entries,

            "zone_visit": zone_visits,

            "dwell": dwell_visitors,

            "queue": queued_visitors,

            "billing": billing,

            "purchase": purchases,

            "exit": exit_count,

            "dropoff_before_billing":
                max(
                    entries - billing,
                    0
                ),

            "dropoff_before_purchase":
                max(
                    billing - purchases,
                    0
                ),
            "abandoned_queue_count": abandoned_queue_count
        }

    finally:

        db.close()