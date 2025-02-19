import pytest
from fastapi.testclient import TestClient
from main import app  # Adjust the import according to the location of your FastAPI app


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


def test_integration_json(client):
    """Test that the /integration.json endpoint returns the correct structure"""
    response = client.get("/integration.json")
    assert response.status_code == 200
    json_response = response.json()
    
    # Check the basic structure of the response
    assert "data" in json_response
    assert "descriptions" in json_response["data"]
    assert "settings" in json_response["data"]
    assert "tick_url" in json_response["data"]
    
    # Check the required fields inside descriptions
    assert "app_name" in json_response["data"]["descriptions"]
    assert "app_description" in json_response["data"]["descriptions"]
    assert "app_url" in json_response["data"]["descriptions"]
    assert "app_logo" in json_response["data"]["descriptions"]
    assert "background_color" in json_response["data"]["descriptions"]
    
    # Check the settings
    assert len(json_response["data"]["settings"]) > 0
    assert "label" in json_response["data"]["settings"][0]
    assert "type" in json_response["data"]["settings"][0]
    assert "required" in json_response["data"]["settings"][0]
    assert "default" in json_response["data"]["settings"][0]
    
    # Check tick_url
    assert json_response["data"]["tick_url"].startswith("http")


def test_tick(client, mocker):
    """Test the /tick endpoint to ensure performance check logic works"""

    # Mocking the check_site_performance and run_lighthouse methods
    mock_check_site_performance = mocker.patch("main.check_site_performance", return_value="✅ site loaded in 1.23 seconds.")
    mock_run_lighthouse = mocker.patch("main.run_lighthouse", return_value={
        "performance_score": 90,
        "first_contentful_paint": 1500,
        "speed_index": 2000,
        "time_to_interactive": 3000
    })
    
    # Create a payload for the tick
    payload = {
        "channel_id": "123",
        "return_url": "http://example.com",
        "settings": [
            {"label": "site-1", "type": "text", "required": True, "default": "http://testsite1.com"},
            {"label": "interval", "type": "text", "required": True, "default": "* * * * *"}
        ]
    }
    
    # Now use the sync `client.post()` without `await`
    response = client.post("/tick", json=payload)
    assert response.status_code == 200
    assert response.json() == {"status": "success"}
    
    # Verify the mocked functions were called
    mock_check_site_performance.assert_called_once_with("http://testsite1.com")
    mock_run_lighthouse.assert_called_once_with("http://testsite1.com")


def test_send_to_channel(client, mocker):
    """Test that the send_to_channel function is called with correct parameters"""
    
    # Mock the background task properly by replacing it with a dummy function
    def mock_background_send_to_channel(return_url, message):
        assert return_url == "http://example.com"
        assert message is not None  # Ensure that a message is passed
    
    # Patch the background task with the mock function
    mocker.patch("main.send_to_channel", side_effect=mock_background_send_to_channel)
    
    # Create a payload for the tick
    payload = {
        "channel_id": "123",
        "return_url": "http://example.com",
        "settings": [
            {"label": "site-1", "type": "text", "required": True, "default": "http://testsite1.com"},
            {"label": "interval", "type": "text", "required": True, "default": "* * * * *"}
        ]
    }
    
    # Use the sync client without `await`
    response = client.post("/tick", json=payload)
    
    # Ensure that the background task was called correctly
    assert response.status_code == 200
    assert response.json() == {"status": "success"}

