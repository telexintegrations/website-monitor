from fastapi import APIRouter, BackgroundTasks
from app.schemas import MonitorPayload
from app.core.utils import check_site_performance, ensure_https
from app.crud import send_to_channel
import time

router = APIRouter()

@router.post("/tick")
def tick(payload: MonitorPayload, background_tasks: BackgroundTasks):
    """Telex calls this route to monitor website performance."""
    # Extract the sites that need to be monitored from the settings
    sites = [ensure_https(s.default) for s in payload.settings if s.label.startswith("site") and s.default]
    
    # Initialize a list to store the results of each site's performance check
    results = []
    
    # Process each site in the payload
    for site in sites:
        # Check performance for each site and append the result
        result = check_site_performance(site)
        results.append(result)
        
        # To avoid hitting API rate limits, introduce a short delay
        # time.sleep(1)
    
    # Combine the results into a single message
    message = "\n\n".join(results)
    
    # Add a background task to send the message to Telex
    background_tasks.add_task(send_to_channel, payload.return_url, message)
    
    # Return a success status response
    return {"status": "success"}
