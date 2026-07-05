from datetime import datetime

RAIN_CHANCE_THRESHOLD = 60  # % chance_of_rain to count as "sap mua"
CURRENT_PRECIP_THRESHOLD_MM = 0.1
LOOKAHEAD_HOURS = 2
RAIN_KEYWORDS = ("mua", "rain", "drizzle", "mưa", "giông", "dông", "thunderstorm")

TIME_FMT = "%Y-%m-%d %H:%M"


def _looks_like_rain(condition_text: str) -> bool:
    text = condition_text.lower()
    return any(keyword in text for keyword in RAIN_KEYWORDS)


def check_point(point: dict, forecast_json: dict) -> dict | None:
    """Return an alert dict if this point shows current or imminent rain, else None."""
    current = forecast_json["current"]
    location = forecast_json["location"]
    hours = forecast_json["forecast"]["forecastday"][0]["hour"]

    now = datetime.strptime(location["localtime"], TIME_FMT)

    current_precip = current.get("precip_mm", 0) or 0
    current_condition = current["condition"]["text"]
    if current_precip >= CURRENT_PRECIP_THRESHOLD_MM or _looks_like_rain(current_condition):
        return {
            "name": point["name"],
            "lat": point["lat"],
            "lon": point["lon"],
            "kind": "dang mua",
            "detail": f"{current_condition}, {current_precip}mm/h",
        }

    upcoming = [h for h in hours if datetime.strptime(h["time"], TIME_FMT) > now]
    upcoming = upcoming[:LOOKAHEAD_HOURS]
    for hour in upcoming:
        chance = hour.get("chance_of_rain", 0) or 0
        if hour.get("will_it_rain") == 1 and chance >= RAIN_CHANCE_THRESHOLD:
            hour_label = datetime.strptime(hour["time"], TIME_FMT).strftime("%H:%M")
            return {
                "name": point["name"],
                "lat": point["lat"],
                "lon": point["lon"],
                "kind": "sap mua",
                "detail": f"{chance}% kha nang mua luc {hour_label} ({hour['condition']['text']})",
            }

    return None
