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

## Telex Integration

To integrate with Telex, configure the webhook URL and ensure the API can communicate with the Telex service.

### Example Telex Message Output

(Screenshot of integration in Telex here)

## License

MIT License

---

For any issues, create a GitHub issue.

