from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
import httpx
import json
import asyncio
import subprocess
from pydantic import BaseModel
from typing import List

app = FastAPI()

@app.get("/integration.json")
def get_integration_json(request: Request):
    """Telex's required json route that defines the integration """
    base_url = str(request.base_url).rstrip("/")
    return {
        "data": {
            "descriptions": {
                "app_name": "Website Monitor",
                "app_description": "Monitors website performance using Lighthouse",
                "app_url": base_url,
                "app_logo": "https://i.imgur.com/lZqvffp.png",
                "background_color": "#ffffff"
            },
            "integration_type": "interval",
            "settings": [
                {"label": "site-1", "type": "text", "required": True, "default": ""},
                {"label": "site-2", "type": "text", "required": False, "default": ""},
                {"label": "interval", "type": "text", "required": True, "default": "* * * * *"}
            ],
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

async def check_site_performance(site: str) -> str:
    """this checks the load speed of the website."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(site, timeout=10)
            load_time = response.elapsed.total_seconds()
            return f"✅ {site} loaded in {load_time:.2f} seconds."
    except Exception as e:
        return f"❌ Failed to load {site}: {str(e)}"

def run_lighthouse(url: str):
    """Runs lighthouse headlessly to get the report for the websites"""
    command = f"lighthouse {url} --quiet --chrome-flags='--headless' --output=json"
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8')
    # print(result)
    try:
        data = json.loads(result.stdout)
        return {
            "performance_score": data["categories"]["performance"]["score"] * 100,
            "first_contentful_paint": data["audits"]["first-contentful-paint"]["numericValue"],
            "speed_index": data["audits"]["speed-index"]["numericValue"],
            "time_to_interactive": data["audits"]["interactive"]["numericValue"],
        }
    except json.JSONDecodeError:
        return {"error": "Failed to parse Lighthouse output"}

async def send_to_channel(return_url: str, message: str):
    """This function sends the performance report to telex"""
    data = {
        "message": message,
        "username": "Website Monitor",
        "event_name": "Performance Check",
        "status": "error"
    }
    async with httpx.AsyncClient() as client:
        await client.post(return_url, json=data)


@app.post("/tick")
async def tick(payload: MonitorPayload, background_tasks: BackgroundTasks):
    """Telex calls this route to monitor website performance."""
    sites = [s.default for s in payload.settings if s.label.startswith("site") and s.default]

    results = []
    for site in sites:
        load_time_result = await check_site_performance(site)
        lighthouse_result = run_lighthouse(site)
        if "error" in lighthouse_result:
            full_result = f"{load_time_result}\n❌ Lighthouse failed: {lighthouse_result['error']}"
        else:
            full_result = f"{load_time_result}\n📊 Lighthouse:\n- Performance score:{lighthouse_result['performance_score']}\n- First contentful paint: {lighthouse_result['first_contentful_paint']} ms\n- Speed Index: {lighthouse_result['speed_index']} ms\n- Time to interactive: {lighthouse_result['time_to_interactive']} ms"
        results.append(full_result)

    message = "\n\n".join(results)
    background_tasks.add_task(send_to_channel, payload.return_url, message)
    # print(message)

    return {"status": "success"}
