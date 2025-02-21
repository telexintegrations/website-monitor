import os
from fastapi import FastAPI, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx
from pydantic import BaseModel
from typing import List
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True, 
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# PAGESPEED_API_KEY = os.getenv("PAGESPEED_API_KEY")
PAGESPEED_API_KEY = "AIzaSyD6g9hkl11tS2L_kKKsTG6nwobnUsA0h1k"
PAGESPEED_API_URL = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"

@app.get("/integration.json")
def get_integration_json(request: Request):
    """Telex's required JSON route that defines the integration."""
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
                {
                    "label": "site-1",
                    "type": "text",
                    "required": True,
                    "default": ""
                },
                {
                    "label": "site-2",
                    "type": "text",
                    "required": False,
                    "default": ""
                },
                {
                    "label": "interval",
                    "type": "text",
                    "required": True,
                    "default": "0 12 * * *"
                }
            ],
            "target_url": f"{base_url}/integration.json",
            "tick_url": f"{base_url}/tick"
        }
    }

class Setting(BaseModel):
    label: str
    type: str
    required: bool
    default: str

class MonitorPayload(BaseModel):
    channel_id: str
    return_url: str
    settings: List[Setting]

def check_site_performance(site: str) -> str:
    """Checks website performance using Google PageSpeed API, focusing on rendering and interactivity."""
    params = {
        "url": site,
        "key": PAGESPEED_API_KEY,
        "strategy": "desktop",
        "category": ["performance", "accessibility", "best-practices", "seo"]
    }
    try:
        response = httpx.get(PAGESPEED_API_URL, params=params, timeout=30)
        data = response.json()
        
        if "lighthouseResult" not in data:
            return f"❌ Failed to analyze {site}: {data.get('error', {}).get('message', 'Unknown error')}"
        
        result = data["lighthouseResult"]
        performance_score = result["categories"]["performance"]["score"] * 100
        accessibility_score = result["categories"]["accessibility"]["score"] * 100
        best_practices_score = result["categories"]["best-practices"]["score"] * 100
        seo_score = result["categories"]["seo"]["score"] * 100
        fcp = result["audits"]["first-contentful-paint"]["numericValue"]
        speed_index = result["audits"]["speed-index"]["numericValue"]
        tti = result["audits"]["interactive"]["numericValue"]
        
        return (f"✅ {site} Analysis:\n"
                f"- Performance Score: {performance_score}\n"
                f"- Accessibility Score: {accessibility_score}\n"
                f"- Best Practices Score: {best_practices_score}\n"
                f"- SEO Score: {seo_score}\n"
                f"- First Contentful Paint (FCP): {fcp} ms\n"
                f"- Speed Index: {speed_index} ms\n"
                f"- Time to Interactive (TTI): {tti} ms\n"
                f"\n(Note: Load time is just one factor; these metrics provide deeper insights into the user experience.)")
    except httpx.TimeoutException:
        return f"❌ Error analyzing {site}: The request timed out. Try again later."
    except Exception as e:
        return f"❌ Error analyzing {site}: {str(e)}"

def send_to_channel(return_url: str, message: str):
    """Sends the performance report to Telex and returns JSON response."""
    print(return_url)
    data = {
        "message": message,
        "username": "Website Monitor",
        "event_name": "Performance Check",
        "status": "success"
    }
    response = httpx.post(return_url, json=data)
    # payload = {
    # "event_name": "string",
    # "message": "python post",
    # "status": "success",
    # "username": "collins"
    # }
    # response = requests.post(
    # url,
    # json=payload,
    # headers={
    #     "Accept": "application/json",
    #     "Content-Type": "application/json"
    # }
    # )
    print(response.json())
    return response.json()

@app.post("/tick")
def tick(payload: MonitorPayload, background_tasks: BackgroundTasks):
    """Telex calls this route to monitor website performance."""
    sites = [s.default for s in payload.settings if s.label.startswith("site") and s.default]
    results = []
    for site in sites:
        result = check_site_performance(site)
        results.append(result)
        time.sleep(2)  # Delay to avoid hitting API rate limits
    
    message = "\n\n".join(results)
    background_tasks.add_task(send_to_channel, payload.return_url, message)
    print(message)
    return {"status": "success"}

