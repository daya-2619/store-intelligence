import random
from typing import Dict, Any, List

class LiveMetricsService:
    @staticmethod
    def get_live_cctv_feeds(store_id: str) -> List[Dict[str, Any]]:
        # Mocked data for the live CCTV dashboard
        return [
            {
                "camera_id": "CAM_1",
                "status": "ONLINE",
                "active_visitors": random.randint(5, 15),
                "queue_size": 0,
                "alerts": []
            },
            {
                "camera_id": "CAM_2",
                "status": "ONLINE",
                "active_visitors": random.randint(10, 25),
                "queue_size": random.randint(0, 3),
                "alerts": ["QUEUE_CONGESTION"] if random.random() > 0.8 else []
            },
            {
                "camera_id": "CAM_3",
                "status": "ONLINE",
                "active_visitors": random.randint(2, 8),
                "queue_size": 0,
                "alerts": ["DEAD_ZONE"] if random.random() > 0.9 else []
            }
        ]

    @staticmethod
    def get_realtime_alerts(store_id: str) -> List[Dict[str, Any]]:
        # Mocked real-time alerts
        alerts = []
        if random.random() > 0.7:
            alerts.append({"type": "QUEUE_CONGESTION", "severity": "CRITICAL", "message": "High queue depth detected at CAM_2"})
        if random.random() > 0.8:
            alerts.append({"type": "LONG_DWELL", "severity": "WARN", "message": "Visitor dwelling > 10m in Zone A"})
        return alerts

live_metrics_service = LiveMetricsService()
