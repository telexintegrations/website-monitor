# Website Monitor

## Overview

Website Monitor is a FastAPI-based application that integrates with Lighthouse and Telex to analyze website performance, accessibility, best practices, and SEO. It provides real-time insights into website performance and sends reports to Telex channels.

## Features

- Analyze website performance using Google's PageSpeed Insights API
- Retrieve key metrics such as performance score, accessibility score, best practices score, and SEO score
- Send results to a Telex channel
- FastAPI-based web application with RESTful endpoints

## Setup Instructions

### Prerequisites

- Python 3.10+
- Virtual environment (recommended)
- API key for PageSpeed Insights (if required)

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/telexintegrations/website-monitor.git
   cd website-monitor
   ```
2. Create a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

### Running the Application

```sh
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## API Endpoints

- `POST /tick` - Analyze a website and send results to a Telex channel.
- `GET /integration.json` - Retrieve integration metadata.

## Testing

Run tests using pytest:

```sh
pytest
```

## Deployment

Deploy using Docker:

```sh
docker build -t website-monitor .
docker run -p 8000:8000 website-monitor
```

Or deploy on AWS EC2, Render, or other cloud providers following best practices.

## API Endpoints
### **1. Get Integration JSON**
Returns the JSON required by Telex.
```sh
GET https://website-monitor-kokv.onrender.com/integration.json
```

### **2. Trigger a Website Check (Telex Tick Event)**
Telex calls this endpoint to perform a scheduled website performance check.
```sh
POST https://website-monitor-kokv.onrender.com/tick
```
#### **Example Payload**
```json
{
    "channel_id": "test_channel",
    "return_url": "https://telex.com/webhook",
    "settings": [
        { "label": "site-1", "type": "text", "required": true, "default": "https://example.com" }
    ]
}
```

#### **Response**
```json
{
    "status": "success"
}
```

## Use Cases
### **1. Monitoring a Website’s Performance in Telex**
- Users integrate this service into **Telex** to receive scheduled reports.
- The bot sends insights on **load speed, SEO, and accessibility**.

### **2. Checking Performance for Multiple Websites**
- The integration supports checking multiple websites in one request.
- Useful for monitoring competitors or various company websites.

### **3. Getting Automated Alerts on Website Speed Drops**
- If a website's speed drops significantly, Telex can notify admins.
- Helps in proactively optimizing website performance.


### Example Telex Message Output
(Screenshot of integration in Telex here)
![image](https://github.com/user-attachments/assets/af6710d8-633d-4ea9-b53f-b78b4c192f09)
![image](https://github.com/user-attachments/assets/e60c65df-c673-4cc4-ae9e-d9bb6b53f70c)




## License

MIT License

---

For any issues, create a GitHub issue.

