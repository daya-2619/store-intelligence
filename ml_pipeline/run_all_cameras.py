from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed
)

from process_video import (
    process_video,
    validate_startup
)

import os
import sys
import time
import urllib.parse

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

PROJECT_ROOT = os.path.normpath(
    os.path.join(
        BASE_DIR,
        ".."
    )
)


def run_all_cameras():

    sys.path.append(PROJECT_ROOT)

    from app.db import SessionLocal
    from app.models import Camera

    while True:

        db = SessionLocal()

        try:

            active_cameras = (

                db.query(Camera)

                .filter(
                    Camera.status == "ONLINE"
                )

                .all()
            )

            camera_tasks = [

                (
                    cam.store_id,
                    cam.camera_id,
                    cam.source_path,
                    cam.stream_url
                )

                for cam in active_cameras
            ]

        finally:

            db.close()

        print(
            f"\nFound {len(camera_tasks)} "
            f"ONLINE cameras in the database registry."
        )

        if not camera_tasks:

            print(
                "No active cameras found. "
                "Waiting 10 seconds..."
            )

            time.sleep(10)

            continue

        workers = len(camera_tasks)

        with ThreadPoolExecutor(
            max_workers=workers
        ) as executor:

            futures = []

            for (
                store_id,
                camera_id,
                source_path,
                stream_url
            ) in camera_tasks:

                video_path = None

                try:

                    # ---------------------------
                    # Priority 1
                    # Use actual source_path
                    # ---------------------------

                    if source_path:

                        video_path = os.path.join(
                            PROJECT_ROOT,
                            source_path
                        )

                        video_path = (
                            os.path.normpath(
                                video_path
                            )
                        )

                    # ---------------------------
                    # Priority 2
                    # Local frontend videos
                    # ---------------------------

                    elif (
                        stream_url
                        and stream_url.startswith(
                            "/videos/"
                        )
                    ):

                        filename = (
                            stream_url.replace(
                                "/videos/",
                                ""
                            )
                        )

                        video_path = os.path.join(
                            PROJECT_ROOT,
                            "frontend",
                            "public",
                            "videos",
                            filename
                        )

                        video_path = (
                            os.path.normpath(
                                video_path
                            )
                        )

                    # ---------------------------
                    # Priority 3
                    # CCTV URL mapping
                    # ---------------------------

                    elif (
                        stream_url
                        and stream_url.startswith(
                            "http://127.0.0.1:8000/cctv/"
                        )
                    ):

                        rel_path = (
                            stream_url.replace(
                                "http://127.0.0.1:8000/cctv/",
                                ""
                            )
                        )

                        rel_path = (
                            urllib.parse.unquote(
                                rel_path
                            )
                        )

                        video_path = os.path.join(
                            PROJECT_ROOT,
                            "data",
                            "CCTV Footage",
                            rel_path
                        )

                        video_path = (
                            os.path.normpath(
                                video_path
                            )
                        )

                    else:

                        print(
                            f"\n❌ No valid source "
                            f"configured for "
                            f"{camera_id}"
                        )

                        continue

                    # ---------------------------
                    # Debug Logs
                    # ---------------------------

                    print(
                        "\n========================"
                    )

                    print(
                        f"Camera : {camera_id}"
                    )

                    print(
                        f"Store  : {store_id}"
                    )

                    print(
                        f"Source : {source_path}"
                    )

                    print(
                        f"Resolved Path : "
                        f"{video_path}"
                    )

                    print(
                        f"Exists : "
                        f"{os.path.exists(video_path)}"
                    )

                    print(
                        "========================\n"
                    )

                    # ---------------------------
                    # Validation
                    # ---------------------------

                    if not os.path.exists(
                        video_path
                    ):

                        print(
                            f"⚠️ Stream source "
                            f"not found for "
                            f"{camera_id}"
                        )

                        continue

                    futures.append(

                        executor.submit(

                            process_video,

                            video_path,

                            store_id,

                            camera_id
                        )
                    )

                except Exception as e:

                    print(
                        f"Failed to start "
                        f"{camera_id}: {e}"
                    )

            for future in as_completed(
                futures
            ):

                try:

                    future.result()

                except Exception as e:

                    print(
                        f"Camera failed: {e}"
                    )

        print(
            "\nAll cameras processed "
            "for this cycle."
        )

        print(
            "Restarting camera scan...\n"
        )


if __name__ == "__main__":

    run_all_cameras()