import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import httpx
from app.main import app
from app.core.utils import check_site_performance
from app.crud import send_to_channel

client = TestClient(app)

@pytest.fixture
def mock_pagespeed_response():
    return {
        "lighthouseResult": {
            "categories": {
                "performance": {"score": 0.85},
                "accessibility": {"score": 0.90},
                "best-practices": {"score": 0.80},
                "seo": {"score": 0.95},
            },
            "audits": {
                "first-contentful-paint": {"numericValue": 1234},
                "speed-index": {"numericValue": 2345},
                "interactive": {"numericValue": 3456},
            },
        }
    }

@patch("httpx.get")
def test_check_site_performance(mock_get, mock_pagespeed_response):
    mock_get.return_value.json.return_value = mock_pagespeed_response
    mock_get.return_value.status_code = 200

    result = check_site_performance("https://example.com")
    assert "Performance Score" in result
    assert "Accessibility Score" in result
    assert "Best Practices Score" in result
    assert "SEO Score" in result
    assert "First Contentful Paint" in result
    assert "Speed Index" in result
    assert "Time to Interactive" in result

@patch("httpx.post")
def test_send_to_channel(mock_post):
    mock_post.return_value.json.return_value = {"status": "success"}
    response = send_to_channel("https://telex.com/webhook", "Test message")
    assert response["status"] == "success"

@patch("app.core.utils.check_site_performance")
def test_tick(mock_check):
    mock_check.return_value = "✅ Test site loaded successfully."
    payload = {
        "channel_id": "test_channel",
        "return_url": "https://ping.telex.im/v1/webhooks/0195189b-9a34-7faa-b8f0-8b76e0dee28f",
        "settings": [{"label": "site-1", "type": "text", "required": True, "default": "https://example.com"}]
    }
    response = client.post("/tick", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_integration_json():
    response = client.get("/integration.json")
    assert response.status_code == 200
    assert "data" in response.json()
    assert "app_name" in response.json()["data"]["descriptions"]
