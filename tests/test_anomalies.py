import pytest
from app.services.anomaly_service import get_anomalies

def test_anomalies_structure():
    anomalies = get_anomalies("ST1008")
    
    assert "anomalies" in anomalies
    assert isinstance(anomalies["anomalies"], list)
    
    # Validate structure if any anomalies exist
    for anomaly in anomalies["anomalies"]:
        assert "type" in anomaly
        assert "severity" in anomaly
        assert "suggested_action" in anomaly
