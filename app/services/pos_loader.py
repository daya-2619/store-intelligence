import pandas as pd

from app.db import SessionLocal
from app.models import POSTransaction


def load_pos_csv(file_path):

    df = pd.read_csv(file_path)

    grouped = df.groupby(["order_id", "store_id", "order_date", "order_time"]).agg({
        "total_amount": "sum"
    }).reset_index()

    db = SessionLocal()
    inserted = 0

    try:
        for _, row in grouped.iterrows():

            timestamp_str = f"{row['order_date']} {row['order_time']}"
            existing = db.query(POSTransaction).filter_by(transaction_id=str(row["order_id"])).first()
            if existing:
                continue

            transaction = POSTransaction(
                store_id=str(row["store_id"]),
                transaction_id=str(row["order_id"]),
                timestamp=pd.to_datetime(timestamp_str, format="%d-%m-%Y %H:%M:%S", utc=True, errors="coerce"),
                basket_value_inr=float(row["total_amount"])
            )

            db.add(transaction)

            inserted += 1

        db.commit()

        return {
            "inserted": inserted
        }

    finally:

        db.close()