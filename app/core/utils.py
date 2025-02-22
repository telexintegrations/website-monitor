import httpx
import os

PAGESPEED_API_KEY = os.getenv("PAGESPEED_API_KEY")
PAGESPEED_API_URL = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"

def check_site_performance(site: str) -> str:
    """Checks website performance using Google PageSpeed API."""
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
                f"\n(Note: These metrics can provide deeper insights into the user experience.)")
    except httpx.TimeoutException:
        return f"❌ Error analyzing {site}: The request timed out. Try again later."
    except Exception as e:
        return f"❌ Error analyzing {site}: {str(e)}"


def ensure_https(url: str) -> str:
    """Ensures the URL starts with 'https://'"""
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url