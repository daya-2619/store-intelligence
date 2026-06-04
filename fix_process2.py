with open('ml_pipeline/process_video.py', 'r') as f:
    code = f.read()

bad_block = '''            conf = detections.confidence[idx] if (detections.confidence is not None and len(detections.confidence) > idx) else 0.95
            state.visitor_confidence[visitor_id] = float(conf)
                
            x1, y1, x2, y2 = bbox
            center_x = (x1 + x2) / 2.0
            center_y = (y1 + y2) / 2.0
            
            visitor_id = f"TRACK_{camera_id}_{track_id}"'''

good_block = '''            x1, y1, x2, y2 = bbox
            center_x = (x1 + x2) / 2.0
            center_y = (y1 + y2) / 2.0
            
            visitor_id = f"TRACK_{camera_id}_{track_id}"

            conf = detections.confidence[idx] if (detections.confidence is not None and len(detections.confidence) > idx) else 0.95
            state.visitor_confidence[visitor_id] = float(conf)'''

code = code.replace(bad_block, good_block)

code = code.replace(
    'abandon_event = create_queue_abandon_event(track_id, prev_zone, store_id, camera_id, global_visitor_id)',
    'abandon_event = create_queue_abandon_event(track_id, prev_zone, store_id, camera_id, global_visitor_id, confidence=conf)'
)

code = code.replace(
    'entry_event = create_reentry_event(track_id, store_id, camera_id, global_visitor_id)',
    'entry_event = create_reentry_event(track_id, store_id, camera_id, global_visitor_id, confidence=conf)'
)

code = code.replace(
    'entry_event = create_entry_event(track_id, store_id, camera_id, global_visitor_id)',
    'entry_event = create_entry_event(track_id, store_id, camera_id, global_visitor_id, confidence=conf)'
)

code = code.replace(
    'exit_event = create_zone_exit_event(track_id, prev_zone, store_id, camera_id, global_visitor_id)',
    'exit_event = create_zone_exit_event(track_id, prev_zone, store_id, camera_id, global_visitor_id, confidence=conf)'
)

code = code.replace(
    'dwell_event = create_dwell_event(track_id, prev_zone, store_id, camera_id, dwell_ms, global_visitor_id)',
    'dwell_event = create_dwell_event(track_id, prev_zone, store_id, camera_id, dwell_ms, global_visitor_id, confidence=conf)'
)

code = code.replace(
    'zone_event = create_zone_event(track_id, zone, store_id, camera_id, global_visitor_id)',
    'zone_event = create_zone_event(track_id, zone, store_id, camera_id, global_visitor_id, confidence=conf)'
)


with open('ml_pipeline/process_video.py', 'w') as f:
    f.write(code)
