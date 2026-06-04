import pytest
from app.services.funnel_service import get_funnel

def test_funnel_stages():
    funnel = get_funnel("ST1008")
    
    assert "entry" in funnel
    assert "billing" in funnel
    assert "abandoned_queue_count" in funnel
    assert "purchase" in funnel
    
    assert funnel["billing"] >= funnel["purchase"]
