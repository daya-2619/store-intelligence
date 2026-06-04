from datetime import timedelta
import uuid

from app.models import (
    VisitorSession,
    BillingVisit,
    POSTransaction,
    Event
)
from app.repositories.session_repository import session_repository
from app.repositories.billing_repository import billing_repository
from app.repositories.transaction_repository import transaction_repository

def handle_session_events_bulk(db, events):
    if not events:
        return
        
    visitor_ids = list({e.visitor_id for e in events})
    store_ids = list({e.store_id for e in events})

    # Fetch existing sessions
    existing_sessions_list = session_repository.get_by_ids(db, visitor_ids, store_ids)
    existing_sessions = {(s.visitor_id, s.store_id): s for s in existing_sessions_list}
    
    # Fetch existing billing visits
    existing_billing = billing_repository.get_by_ids(db, visitor_ids)
    billing_set = {(b.visitor_id, b.store_id) for b in existing_billing}

    # Fetch POS transactions within the batch window
    min_time = min(e.timestamp for e in events)
    max_time = max(e.timestamp for e in events) + timedelta(minutes=5)
    
    pos_txns = transaction_repository.get_in_time_range(db, store_ids, min_time, max_time)

    new_sessions = []
    new_billing_visits = []
    new_abandon_events = []

    for event in events:
        session = existing_sessions.get((event.visitor_id, event.store_id))
        if not session:
            session = VisitorSession(
                visitor_id=event.visitor_id,
                store_id=event.store_id,
                entry_time=event.timestamp,
                is_staff=event.is_staff,
                converted=False
            )
            existing_sessions[(event.visitor_id, event.store_id)] = session
            new_sessions.append(session)

        # EXIT event or exiting the BILLING zone
        if event.event_type == "EXIT" or (event.event_type == "ZONE_ENTER" and event.zone_id != "BILLING"):
            if event.event_type == "EXIT":
                session.exit_time = event.timestamp

            # Queue Abandonment Logic:
            if not session.converted and (event.visitor_id, event.store_id) in billing_set:
                if not any(e.visitor_id == event.visitor_id and e.event_type == "BILLING_QUEUE_ABANDON" for e in new_abandon_events):
                    new_abandon_events.append(Event(
                        event_id=str(uuid.uuid4()),
                        store_id=event.store_id,
                        camera_id=event.camera_id,
                        visitor_id=event.visitor_id,
                        event_type="BILLING_QUEUE_ABANDON",
                        zone_id="BILLING",
                        timestamp=event.timestamp,
                        dwell_ms=0,
                        is_staff=event.is_staff,
                        confidence=1.0,
                        event_metadata={}
                    ))

        # BILLING ZONE handling
        if event.event_type == "ZONE_ENTER" and event.zone_id == "BILLING":
            if (event.visitor_id, event.store_id) not in billing_set:
                new_billing_visits.append(BillingVisit(
                    visitor_id=event.visitor_id,
                    store_id=event.store_id,
                    billing_enter_time=event.timestamp
                ))
                billing_set.add((event.visitor_id, event.store_id))

            # POS Correlation Logic
            if not session.converted:
                matched_txn = next(
                    (t for t in pos_txns if t.store_id == event.store_id and 
                     event.timestamp <= t.timestamp <= event.timestamp + timedelta(minutes=5)),
                    None
                )
                if matched_txn:
                    session.converted = True
                    pos_txns.remove(matched_txn)

    if new_sessions:
        db.add_all(new_sessions)
    if new_billing_visits:
        db.add_all(new_billing_visits)
    if new_abandon_events:
        db.add_all(new_abandon_events)
        db.flush()