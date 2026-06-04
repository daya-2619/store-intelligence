import re

with open('ml_pipeline/process_video.py', 'r') as f:
    code = f.read()

# 1. Add confidence extraction
conf_code = """
            if track_id is None:
                continue
                
            conf = detections.confidence[idx] if (detections.confidence is not None and len(detections.confidence) > idx) else 0.95
            state.visitor_confidence[visitor_id] = float(conf)
"""
code = code.replace("""
            if track_id is None:
                continue
""", conf_code)

# 2. Add continuous dwell emission
dwell_code = """
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
"""
code = code.replace("""
                if zone == "BILLING" and prev_zone != "BILLING":
                    vid = global_visitor_id or visitor_id
                    state.queue_start_time[vid] = frame_idx
                    queue_event = create_queue_event(track_id, zone, store_id, camera_id, global_visitor_id)
                    if queue_event:
                        queue_event["event_type"] = "BILLING_QUEUE_JOIN"
                        events_to_send.append(queue_event)
""", dwell_code)

# 3. Replace all create_*(...) with create_*(..., confidence=conf)
# Using regex to capture arguments and append confidence=conf
def repl_call(match):
    name = match.group(1)
    args = match.group(2)
    # create_exit_event is outside the tracking loop, so confidence will be fetched from state
    if name == 'create_exit_event':
        return f'conf = state.visitor_confidence.get(visitor_id, 0.95)\n        exit_event = {name}({args}, confidence=conf)'
    return f'{name}({args}, confidence=conf)'

# Find all create_* calls EXCEPT the one in create_exit_event which needs different scope handling
code = re.sub(r'(create_[a_z_]+_event)\((.*?)\)', repl_call, code)

# Let's fix the exit_event replacement which might end up like `exit_event = conf = state... exit_event = ...`
# Let's revert that and just do a manual string replace
code = code.replace('conf = state.visitor_confidence.get(visitor_id, 0.95)\n        exit_event = create_exit_event', 'create_exit_event')
code = code.replace('exit_event = create_exit_event(track_id, store_id, camera_id, global_visitor_id, confidence=conf)', 
                    'conf = state.visitor_confidence.get(visitor_id, 0.95)\n        exit_event = create_exit_event(track_id, store_id, camera_id, global_visitor_id, confidence=conf)')

with open('ml_pipeline/process_video.py', 'w') as f:
    f.write(code)
