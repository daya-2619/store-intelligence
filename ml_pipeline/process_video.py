import os
import sys
import json
import time
import requests
import logging
from pythonjsonlogger import jsonlogger
import cv2
from ultralytics import YOLO
import supervision as sv

logger = logging.getLogger("process_video")
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s')
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ml_pipeline.zones import get_zone
from ml_pipeline.event_generator import (
    create_entry_event,
    create_exit_event,
    create_zone_event,
    create_zone_exit_event,
    create_dwell_event,
    create_queue_event,
    create_queue_abandon_event,
    create_reentry_event
)
from ml_pipeline.state_manager import StoreStateManager
from ml_pipeline.heatmap_generator import generate_heatmap
from ml_pipeline.reid import get_embedding, match_embedding
from ml_pipeline.event_producer import push_events_to_queue
from ml_pipeline.staff_service import detect_staff
from ml_pipeline.movement_tracker import save_point, track_points

def validate_startup():
    print("Validating CV Pipeline dependencies...")
    try:
        import ultralytics
        import supervision
        return True
    except ImportError as e:
        print(f"Missing dependency: {e}")
        return False

def get_store_config(store_id):
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from app.db import SessionLocal
    from app.models import StoreLayout
    db = SessionLocal()
    try:
        layout = db.query(StoreLayout).filter(StoreLayout.store_id == store_id).first()
        if layout:
            # layout_path e.g. "data/CCTV Footage/Store 1/..."
            base_dir = os.path.dirname(os.path.abspath(__file__))
            abs_path = os.path.join(base_dir, "..", layout.layout_path)
            return {"layout_path": abs_path}
    finally:
        db.close()
    return {}

def process_video(video_path, store_id, camera_id):
    print(f"========== Starting CV Pipeline for {camera_id} ==========")
    
    store_config = get_store_config(store_id)
    
    # Thread-local instantiation to prevent PyTorch Conv.bn race conditions and ByteTrack state contamination
    yolo_model = YOLO("yolov8n.pt")
    yolo_model.fuse() # Pre-fuse to ensure thread safety
    tracker = sv.ByteTrack()
    
    state = StoreStateManager(store_id)
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Failed to open {video_path}")
        return

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0

    events_to_send = []
    
    frame_idx = 0
    stride = 5 
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        frame_idx += 1
        
        if frame_idx % stride != 0:
            continue
            
        # Detect
        results = yolo_model(frame, classes=[0], conf=0.4, verbose=False)[0]
        detections = sv.Detections.from_ultralytics(results)
        
        # Track
        detections = tracker.update_with_detections(detections)
        
        for idx in range(len(detections)):
            bbox = detections.xyxy[idx]
            track_id = detections.tracker_id[idx]
            if track_id is None:
                continue
                
            x1, y1, x2, y2 = bbox
            center_x = (x1 + x2) / 2.0
            center_y = (y1 + y2) / 2.0
            
            visitor_id = f"TRACK_{camera_id}_{track_id}"

            conf = detections.confidence[idx] if (detections.confidence is not None and len(detections.confidence) > idx) else 0.95
            state.visitor_confidence[visitor_id] = float(conf)
            
            # Re-ID Extraction for New Tracks
            if visitor_id not in state.active_tracks:
                state.active_tracks[visitor_id] = True
                
                # Extract Crop safely
                h, w = frame.shape[:2]
                cx1, cy1 = max(0, int(x1)), max(0, int(y1))
                cx2, cy2 = min(w, int(x2)), min(h, int(y2))
                
                if cx2 > cx1 and cy2 > cy1:
                    crop = frame[cy1:cy2, cx1:cx2]
                    emb = get_embedding(crop)
                    
                    if emb is not None:
                        # Match against global memory
                        matched_id, score = match_embedding(emb, state.global_embeddings)
                        if matched_id:
                            state.local_to_global[visitor_id] = matched_id
                            print(f"Re-ID MATCH: {visitor_id} -> {matched_id} (score: {score:.2f})")
                        else:
                            import ml_pipeline.state_manager as sm
                            new_val = sm.global_id_counter_obj.increment()
                            new_global_id = f"GLOBAL_VISITOR_{new_val:03d}"
                            state.local_to_global[visitor_id] = new_global_id
                            state.global_embeddings[new_global_id] = emb.tolist()
                            print(f"Re-ID NEW: {visitor_id} -> {new_global_id}")

            global_visitor_id = state.local_to_global.get(visitor_id)

            # 1.2 Update process_video.py: Add save_point
            save_point(global_visitor_id or visitor_id, center_x, center_y)
            
            # Determine zone
            bottom_center_x = center_x
            bottom_center_y = y2
            zone = get_zone(bottom_center_x, bottom_center_y)
            if not zone:
                zone = "FLOOR"
                
            # If new track -> ENTRY
            if visitor_id not in state.active_tracks or getattr(state.active_tracks, 'get', lambda k: None)(visitor_id) is True:
                # Need to track if entry event sent. active_tracks[visitor_id] is True initially, set to 'sent'
                if state.active_tracks[visitor_id] is True:
                    state.active_tracks[visitor_id] = "sent"
                    if global_visitor_id and global_visitor_id in state.exited_globals:
                        entry_event = create_reentry_event(track_id, store_id, camera_id, global_visitor_id, confidence=conf)
                        state.exited_globals.remove(global_visitor_id)
                    else:
                        entry_event = create_entry_event(track_id, store_id, camera_id, global_visitor_id, confidence=conf)
                    if entry_event:
                        events_to_send.append(entry_event)
                        
            # Run Staff Detection
            detect_staff(global_visitor_id or visitor_id, state)
                
            # Zone state machine
            prev_zone = state.visitor_zone_state.get(visitor_id)
            if zone != prev_zone:
                # Exiting old zone: check dwell
                if prev_zone:
                    exit_event = create_zone_exit_event(track_id, prev_zone, store_id, camera_id, global_visitor_id, confidence=conf)
                    if exit_event:
                        events_to_send.append(exit_event)
                        
                    if prev_zone in state.zone_entry_time.get(visitor_id, {}):
                        dwell_frames = frame_idx - state.zone_entry_time[visitor_id][prev_zone]
                        dwell_ms = int((dwell_frames / fps) * 1000)
                        if dwell_ms > 2000:
                            dwell_event = create_dwell_event(track_id, prev_zone, store_id, camera_id, dwell_ms, global_visitor_id, confidence=conf)
                            if dwell_event:
                                events_to_send.append(dwell_event)
                
                # Entering new zone
                zone_event = create_zone_event(track_id, zone, store_id, camera_id, global_visitor_id, confidence=conf)
                if zone_event:
                    events_to_send.append(zone_event)
                    
                    times = state.zone_entry_time.get(visitor_id, {})
                    times[zone] = frame_idx
                    state.zone_entry_time[visitor_id] = times
                    
                    state.visitor_zone_state[visitor_id] = zone
                    
                # Leaving queue check
                if prev_zone == "BILLING" and zone != "BILLING":
                    vid = global_visitor_id or visitor_id
                    if vid in state.queue_start_time:
                        if not state.visitor_purchased.get(vid, False):
                            abandon_event = create_queue_abandon_event(track_id, prev_zone, store_id, camera_id, global_visitor_id, confidence=conf)
                            if abandon_event:
                                events_to_send.append(abandon_event)
                        del state.queue_start_time[vid]
                        
                # Queue check (Joining)
                if zone == "BILLING" and prev_zone != "BILLING":
                    vid = global_visitor_id or visitor_id
                    state.queue_start_time[vid] = frame_idx
                    queue_event = create_queue_event(track_id, zone, store_id, camera_id, global_visitor_id, confidence=conf)
                    if queue_event:
                        queue_event["event_type"] = "BILLING_QUEUE_JOIN"
                        events_to_send.append(queue_event)

            # --- CONTINUOUS DWELL CHECK ---
            if zone:
                entry_time = state.zone_entry_time.get(visitor_id, {}).get(zone)
                if entry_time:
                    last_emit = state.last_dwell_emit_time.get(visitor_id, {}).get(zone, entry_time)
                    frames_since_last = frame_idx - last_emit
                    if frames_since_last >= 30 * fps:
                        dwell_ms = int(((frame_idx - entry_time) / fps) * 1000)
                        dwell_event = create_dwell_event(track_id, zone, store_id, camera_id, dwell_ms, global_visitor_id, confidence=conf)
                        if dwell_event:
                            events_to_send.append(dwell_event)
                        
                        emit_times = state.last_dwell_emit_time.get(visitor_id, {})
                        emit_times[zone] = frame_idx
                        state.last_dwell_emit_time[visitor_id] = emit_times

    cap.release()
    
    # Generate exit events
    for visitor_id in list(state.active_tracks.keys()):
        if camera_id not in visitor_id:
            continue
        
        # Extrapolate track_id
        track_id = int(visitor_id.split("_")[-1])
        
        global_visitor_id = state.local_to_global.get(visitor_id)
        
        if global_visitor_id:
            state.exited_globals.add(global_visitor_id)
            
        exit_event = create_exit_event(track_id, store_id, camera_id, global_visitor_id)
        if exit_event:
            events_to_send.append(exit_event)
            del state.active_tracks[visitor_id]
            
    # 1.3 Create Heatmap Generator hook
    print(f"Generating heatmap for {camera_id}")
    all_points = []
    for vid, pts in track_points.items():
        if camera_id in vid:
            all_points.extend(pts)
            
    if all_points:
        layout_path = store_config.get("layout_path")
        overlay = generate_heatmap(all_points, (frame_height, frame_width, 3), layout_path)
        heatmaps_dir = os.path.join(os.path.dirname(__file__), "..", "heatmaps")
        os.makedirs(heatmaps_dir, exist_ok=True)
        cv2.imwrite(os.path.join(heatmaps_dir, f"{store_id}.png"), overlay)

    print(f"[{camera_id}] Pushing {len(events_to_send)} events to RabbitMQ")
    if events_to_send:
        for event in events_to_send:
            if state.staff_candidates.get(event["visitor_id"], 0) > 500:
                event["is_staff"] = True
                
        for i in range(0, len(events_to_send), 500):
            batch = events_to_send[i:i+500]
            try:
                success = push_events_to_queue(batch)
                if not success:
                    print("RabbitMQ publish failed.")
            except Exception as e:
                print(f"Publish failed: {e}")

    print(f"Finished {camera_id}")
