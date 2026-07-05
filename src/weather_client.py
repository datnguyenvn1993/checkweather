import requests

BASE_URL = "https://api.weatherapi.com/v1/forecast.json"
TIMEOUT_SECONDS = 10


def get_forecast(lat: float, lon: float, api_key: str) -> dict:
    """Fetch current + hourly forecast for a coordinate. Raises on network/HTTP error."""
    params = {
        "key": api_key,
        "q": f"{lat},{lon}",
        "days": 1,
        "aqi": "no",
        "alerts": "no",
        "lang": "vi",
    }
    resp = requests.get(BASE_URL, params=params, timeout=TIMEOUT_SECONDS)
    resp.raise_for_status()
    return resp.json()
