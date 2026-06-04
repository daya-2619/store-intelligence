import sys
import time
sys.path.insert(0, '.')
import uuid
import random
from datetime import datetime, timezone
from app.db import SessionLocal
from app.models import VisitorSession, POSTransaction

def run():
    while True:
        db = SessionLocal()
        try:
            # Only fetch sessions that haven't converted yet
            sessions = db.query(VisitorSession).filter(VisitorSession.converted == False).all()
            count = 0

            for s in sessions:
                if random.random() > 0.5:
                    s.converted = True
                    pos = POSTransaction(
                        store_id=s.store_id, 
                        transaction_id=str(uuid.uuid4()), 
                        timestamp=s.entry_time or datetime.now(timezone.utc), 
                        basket_value_inr=random.uniform(500, 5000)
                    )
                    db.add(pos)
                    count += 1

            db.commit()
            if count > 0:
                print(f'Added {count} mock transactions!')
        except Exception as e:
            print(f"Error: {e}")
            db.rollback()
        finally:
            db.close()
        
        # Sleep before checking for new sessions
        time.sleep(10)

if __name__ == "__main__":
    run()
