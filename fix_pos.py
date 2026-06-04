from app.db import SessionLocal
from app.models import POSTransaction

db = SessionLocal()
txs = db.query(POSTransaction).all()
count = 0
for t in txs[:len(txs)//2]:
    t.store_id = 'ST1009'
    count += 1
db.commit()
db.close()
print(f'Moved {count} transactions to ST1009')
