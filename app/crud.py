import httpx

def send_to_channel(return_url: str, message: str):
    """Sends the performance report to Telex and returns JSON response."""
    data = {
        "message": message,
        "username": "Website Monitor",
        "event_name": "Performance Check",
        "status": "success"
    }
    response = httpx.post(return_url, json=data)
    return response.json()
