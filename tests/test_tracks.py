import os
from src.core.config import CONFIG

def test_specific_tracks():
    os.environ["EVIDENCE_TRACK"] = "stable"
    os.environ["PROPERTY_TRACK"] = "insider"
    assert CONFIG.get_agent_track("evidence") == "stable"
    assert CONFIG.get_agent_track("property") == "insider"

def test_default_fallback():
    if "PROPERTY_TRACK" in os.environ:
        del os.environ["PROPERTY_TRACK"]
    os.environ["TRACK"] = "insider"
    assert CONFIG.get_agent_track("property") == "insider"
