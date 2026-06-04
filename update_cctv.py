import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from sqlalchemy import text
from app.db import SessionLocal, engine
from app.models import Camera, Store, StoreLayout, Base

# Create new tables if they don't exist
Base.metadata.create_all(bind=engine)

DATASET_CONFIG = {
    "ST1008": {
        "layout": "data/CCTV Footage/Store 1/Store 1 - layout.png",
        "cameras": [
            {
                "id": "ST1008_ZONE_CAM_1",
                "name": "CAM 1 - zone",
                "type": "ZONE",
                "source": "data/CCTV Footage/Store 1/CAM 1 - zone.mp4"
            },
            {
                "id": "ST1008_ZONE_CAM_2",
                "name": "CAM 2 - zone",
                "type": "ZONE",
                "source": "data/CCTV Footage/Store 1/CAM 2 - zone.mp4"
            },
            {
                "id": "ST1008_ENTRY_CAM",
                "name": "CAM 3 - entry",
                "type": "ENTRY",
                "source": "data/CCTV Footage/Store 1/CAM 3 - entry.mp4"
            },
            {
                "id": "ST1008_BILLING_CAM",
                "name": "CAM 5 - billing",
                "type": "BILLING",
                "source": "data/CCTV Footage/Store 1/CAM 5 - billing.mp4"
            }
        ]
    },
    "ST1009": {
        "layout": "data/CCTV Footage/Store 2/store 2 - layout.png",
        "cameras": [
            {
                "id": "ST1009_ENTRY_CAM_1",
                "name": "entry 1",
                "type": "ENTRY",
                "source": "data/CCTV Footage/Store 2/entry 1.mp4"
            },
            {
                "id": "ST1009_ENTRY_CAM_2",
                "name": "entry 2",
                "type": "ENTRY",
                "source": "data/CCTV Footage/Store 2/entry 2.mp4"
            },
            {
                "id": "ST1009_ZONE_CAM",
                "name": "zone",
                "type": "ZONE",
                "source": "data/CCTV Footage/Store 2/zone.mp4"
            },
            {
                "id": "ST1009_BILLING_CAM",
                "name": "billing_area",
                "type": "BILLING",
                "source": "data/CCTV Footage/Store 2/billing_area.mp4"
            }
        ]
    }
}

db = SessionLocal()
try:
    # Migrate schema
    try:
        db.execute(text("ALTER TABLE stores ADD COLUMN IF NOT EXISTS layout_path VARCHAR;"))
        db.execute(text("ALTER TABLE cameras ADD COLUMN IF NOT EXISTS camera_name VARCHAR;"))
        db.execute(text("ALTER TABLE cameras ADD COLUMN IF NOT EXISTS camera_type VARCHAR;"))
        db.execute(text("ALTER TABLE cameras ADD COLUMN IF NOT EXISTS zone_name VARCHAR;"))
        db.execute(text("ALTER TABLE cameras ADD COLUMN IF NOT EXISTS is_heatmap_enabled BOOLEAN DEFAULT TRUE;"))
        db.commit()
        print("Migrated database schema.")
    except Exception as e:
        db.rollback()
        print(f"Migration error (ignoring if columns exist): {e}")

    # Remove old cameras and layouts
    db.query(Camera).delete()
    db.query(StoreLayout).delete()

    for store_id, config in DATASET_CONFIG.items():
        # Update Store layout_path
        store = db.query(Store).filter(Store.store_id == store_id).first()
        if store:
            store.layout_path = config["layout"]
        
        # Add StoreLayout record
        db.add(StoreLayout(
            store_id=store_id,
            layout_path=config["layout"],
            width=1920,
            height=1080
        ))

        # Add Cameras
        for cam_config in config["cameras"]:
            # Reconstruct stream_url assuming it's available via /cctv static mount
            # source path is "data/CCTV Footage/Store 1/..."
            # stream_url should be "http://127.0.0.1:8000/cctv/Store 1/..."
            
            cctv_prefix = "data/CCTV Footage/"
            source_path = cam_config["source"]
            
            if source_path.startswith(cctv_prefix):
                rel_path = source_path[len(cctv_prefix):]
                stream_url = f"http://127.0.0.1:8000/cctv/{rel_path}"
            else:
                stream_url = source_path
                
            db.add(Camera(
                camera_id=cam_config["id"],
                store_id=store_id,
                camera_name=cam_config["name"],
                camera_type=cam_config["type"],
                status="ONLINE",
                stream_url=stream_url,
                source_path=source_path,
                is_heatmap_enabled=True
            ))

    db.commit()
    print("Updated Camera stream URLs and Store Layouts dynamically!")
finally:
    db.close()
