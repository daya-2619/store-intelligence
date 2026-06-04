from sqlalchemy import func

from app.db import SessionLocal
from app.models import POSTransaction


def get_pos_summary(store_id: str):

    db = SessionLocal()

    try:

        orders = (
            db.query(
                func.count(
                    func.distinct(
                        POSTransaction.transaction_id
                    )
                )
            )
            .filter(POSTransaction.store_id == store_id)
            .scalar()
        )

        revenue = (
            db.query(
                func.sum(
                    POSTransaction.basket_value_inr
                )
            )
            .filter(POSTransaction.store_id == store_id)
            .scalar()
        )

        products_sold = 0

        avg_order_value = 0

        if orders and orders > 0:
            avg_order_value = (
                revenue or 0
            ) / orders

        return {
            "orders": orders or 0,
            "revenue": round(
                revenue or 0,
                2
            ),
            "products_sold": products_sold or 0,
            "avg_order_value": round(
                avg_order_value,
                2
            )
        }

    except Exception as e:

        return {
            "error": str(e)
        }

    finally:
        db.close()