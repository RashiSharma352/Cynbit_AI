import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))
from engine import analyse_inquiry

def test_analysis_returns_expected_fields():
    result = analyse_inquiry("We need an AI agent for customer support and lead qualification.")
    assert result["category"] in ["AI Automation", "Web & Mobile Development", "Cloud & Infrastructure", "CRM & Marketing Automation", "Product & Platform Inquiry", "General Support"]
    assert result["priority"] in ["High", "Medium", "Low"]
    assert 0 <= result["confidence"] <= 1
    assert result["suggested_reply"]

def test_urgent_priority():
    result = analyse_inquiry("Our production is down and we need urgent cloud support immediately.")
    assert result["priority"] == "High"

def test_short_input_rejected():
    try:
        analyse_inquiry("hi")
        assert False, "Expected ValueError"
    except ValueError:
        assert True
