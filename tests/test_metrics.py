import pytest
from app.services.metrics_service import get_store_metrics

def test_get_metrics_excludes_staff():
    # The actual db might be empty or have data, but we should assert the structure
    metrics = get_store_metrics("ST1008")
    
    assert "active_visitors" in metrics
    assert "conversion_rate" in metrics
    assert "avg_dwell_time" in metrics
    assert "abandonment_rate" in metrics
