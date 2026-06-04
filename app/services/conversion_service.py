from datetime import timedelta

from app.db import SessionLocal

from app.models import (
    BillingVisit,
    VisitorSession,
    Event
)


def mark_conversion(transaction):

    db = SessionLocal()

    start_window = (
        transaction.timestamp
        - timedelta(minutes=5)
    )

    # A visitor who was in the billing zone in the 5-minute window before a transaction timestamp counts as a converted visitor
    recent_billing_event = (

        db.query(Event)

        .filter(
            Event.store_id == transaction.store_id,
            Event.zone_id == "BILLING",
            Event.timestamp >= start_window,
            Event.timestamp <= transaction.timestamp
        )

        .order_by(
            Event.timestamp.desc()
        )

        .first()
    )

    if recent_billing_event:

        session = (

            db.query(VisitorSession)

            .filter(
                VisitorSession.visitor_id
                == recent_billing_event.visitor_id
            )

            .first()
        )

        if session:
            session.converted = True

    db.commit()
    db.close()