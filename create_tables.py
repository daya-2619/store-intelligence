from app.db import (
    engine,
    SessionLocal
)

from app.models import (
    Base,
    Store,
    Camera
)

Base.metadata.create_all(
    bind=engine
)

print(
    "Tables Created Successfully"
)

db = SessionLocal()

try:

    # ----------------------------
    # Seed Stores
    # ----------------------------

    if db.query(Store).count() == 0:

        stores = [

            Store(
                store_id="ST1008",
                store_name="Bangalore Flagship",
                city="Bangalore",
                region="South",
                layout_path=(
                    "data/CCTV Footage/"
                    "Store 1/"
                    "Store 1 - layout.png"
                )
            ),

            Store(
                store_id="ST1009",
                store_name="Mumbai Central",
                city="Mumbai",
                region="West",
                layout_path=(
                    "data/CCTV Footage/"
                    "Store 2/"
                    "store 2 - layout.png"
                )
            )
        ]

        db.add_all(stores)

        db.commit()

        print(
            "Stores seeded successfully."
        )

    # ----------------------------
    # Seed Cameras
    # ----------------------------

    if db.query(Camera).count() == 0:

        cameras = [

            # ====================
            # ST1008
            # ====================

            Camera(
                camera_id="ST1008_ZONE_CAM_1",
                store_id="ST1008",
                camera_name="CAM 1 - zone",
                camera_type="ZONE",
                zone_name="ZONE",
                status="ONLINE",

                source_path=(
                    "data/CCTV Footage/"
                    "Store 1/"
                    "CAM 1 - zone.mp4"
                ),

                stream_url=(
                    "/cctv/"
                    "Store 1/"
                    "CAM 1 - zone.mp4"
                ),

                is_heatmap_enabled=True
            ),

            Camera(
                camera_id="ST1008_ZONE_CAM_2",
                store_id="ST1008",
                camera_name="CAM 2 - zone",
                camera_type="ZONE",
                zone_name="ZONE",
                status="ONLINE",

                source_path=(
                    "data/CCTV Footage/"
                    "Store 1/"
                    "CAM 2 - zone.mp4"
                ),

                stream_url=(
                    "/cctv/"
                    "Store 1/"
                    "CAM 2 - zone.mp4"
                ),

                is_heatmap_enabled=True
            ),

            Camera(
                camera_id="ST1008_ENTRY_CAM",
                store_id="ST1008",
                camera_name="CAM 3 - entry",
                camera_type="ENTRY",
                zone_name="ENTRY",
                status="ONLINE",

                source_path=(
                    "data/CCTV Footage/"
                    "Store 1/"
                    "CAM 3 - entry.mp4"
                ),

                stream_url=(
                    "/cctv/"
                    "Store 1/"
                    "CAM 3 - entry.mp4"
                ),

                is_heatmap_enabled=False
            ),

            Camera(
                camera_id="ST1008_BILLING_CAM",
                store_id="ST1008",
                camera_name="CAM 5 - billing",
                camera_type="BILLING",
                zone_name="BILLING",
                status="ONLINE",

                source_path=(
                    "data/CCTV Footage/"
                    "Store 1/"
                    "CAM 5 - billing.mp4"
                ),

                stream_url=(
                    "/cctv/"
                    "Store 1/"
                    "CAM 5 - billing.mp4"
                ),

                is_heatmap_enabled=True
            ),

            # ====================
            # ST1009
            # ====================

            Camera(
                camera_id="ST1009_ENTRY_CAM_1",
                store_id="ST1009",
                camera_name="entry 1",
                camera_type="ENTRY",
                zone_name="ENTRY",
                status="ONLINE",

                source_path=(
                    "data/CCTV Footage/"
                    "Store 2/"
                    "entry 1.mp4"
                ),

                stream_url=(
                    "/cctv/"
                    "Store 2/"
                    "entry 1.mp4"
                ),

                is_heatmap_enabled=False
            ),

            Camera(
                camera_id="ST1009_ENTRY_CAM_2",
                store_id="ST1009",
                camera_name="entry 2",
                camera_type="ENTRY",
                zone_name="ENTRY",
                status="ONLINE",

                source_path=(
                    "data/CCTV Footage/"
                    "Store 2/"
                    "entry 2.mp4"
                ),

                stream_url=(
                    "/cctv/"
                    "Store 2/"
                    "entry 2.mp4"
                ),

                is_heatmap_enabled=False
            ),

            Camera(
                camera_id="ST1009_ZONE_CAM",
                store_id="ST1009",
                camera_name="zone",
                camera_type="ZONE",
                zone_name="ZONE",
                status="ONLINE",

                source_path=(
                    "data/CCTV Footage/"
                    "Store 2/"
                    "zone.mp4"
                ),

                stream_url=(
                    "/cctv/"
                    "Store 2/"
                    "zone.mp4"
                ),

                is_heatmap_enabled=True
            ),

            Camera(
                camera_id="ST1009_BILLING_CAM",
                store_id="ST1009",
                camera_name="billing_area",
                camera_type="BILLING",
                zone_name="BILLING",
                status="ONLINE",

                source_path=(
                    "data/CCTV Footage/"
                    "Store 2/"
                    "billing_area.mp4"
                ),

                stream_url=(
                    "/cctv/"
                    "Store 2/"
                    "billing_area.mp4"
                ),

                is_heatmap_enabled=True
            )
        ]

        db.add_all(cameras)

        db.commit()

        print(
            "8 Cameras seeded successfully."
        )

finally:

    db.close()