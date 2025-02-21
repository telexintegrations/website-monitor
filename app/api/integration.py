from fastapi import APIRouter, Request
from app.schemas import Setting

router = APIRouter()

@router.get("/integration.json")
def get_integration_json(request: Request):
    base_url = str(request.base_url).rstrip("/")
    return {
        "data": {
            "date": {
                "created_at": "2025-02-19",
                "updated_at": "2025-02-19"
            },
            "descriptions": {
                "app_name": "Website Monitor",
                "app_description": "Monitors website performance using Google PageSpeed API",
                "app_logo": f"{base_url}/static/app_logo.png",
                "app_url": f"{base_url}/integration.json",
                "background_color": "#fff"
            },
            "is_active": True,
            "integration_category": "Website Uptime",
            "integration_type": "interval",
            "key_features": [
                "Analyzes website performance using Google PageSpeed API.",
                "Retrieves key performance metrics such as Performance Score, First Contentful Paint (FCP), Speed Index, and Time to Interactive (TTI).",
                "Provides insights beyond simple load time by evaluating rendering and interactivity metrics."
            ],
            "author": "Lamido",
            "settings": [
                {"label": "site-1", "type": "text", "required": True, "default": ""},
                {"label": "site-2", "type": "text", "required": False, "default": ""},
                {"label": "interval", "type": "text", "required": True, "default": "0 12 * * *"}
            ],
            "target_url": f"{base_url}/integration.json",
            "tick_url": f"{base_url}/tick"
        }
    }
