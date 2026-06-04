import queue
import threading
from typing import Dict, Any
from app.core.events.event_router import EventRouter

class EventProcessor:
    def __init__(self):
        self._queue = queue.Queue()
        self._worker_thread = threading.Thread(target=self._worker, daemon=True)
        self._worker_thread.start()
        self.router = EventRouter()

    def _worker(self):
        while True:
            event = self._queue.get()
            if event is None:
                break
            try:
                self.router.route_event(event)
            except Exception as e:
                print(f"Error processing event: {e}")
            finally:
                self._queue.task_done()

    def process_event(self, event_data: Dict[str, Any]):
        self._queue.put(event_data)

    def shutdown(self):
        self._queue.put(None)
        self._worker_thread.join()

# Global instance for use by ML pipeline scripts
event_processor = EventProcessor()
