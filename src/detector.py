from datetime import datetime

RAIN_CHANCE_THRESHOLD = 85  # % chance_of_rain to count as "sap mua"
CURRENT_PRECIP_THRESHOLD_MM = 0.5
HEAVY_RAIN_MM = 4.0
MODERATE_RAIN_MM = 1.0
LOOKAHEAD_HOURS = 2

# Neu condition text la mot trong cac gia tri "troi quang" nay, khong bao "dang
# mua" du precip_mm vuot nguong - vi precip_mm co the la so lieu tich luy cu,
# tre so voi thoi tiet thuc te hien tai.
CLEAR_CONDITIONS = {"nắng", "trời quang", "sunny", "clear"}

# Ordered from most to least severe; used to sort groups in the alert output.
LEVEL_ORDER = ["Mua to", "Mua vua", "Mua nhe", "Sap mua"]

TIME_FMT = "%Y-%m-%d %H:%M"


def _looks_clear(condition_text: str) -> bool:
    return condition_text.strip().lower() in CLEAR_CONDITIONS


def _current_rain_level(precip_mm: float) -> str:
    if precip_mm >= HEAVY_RAIN_MM:
        return "Mua to"
    if precip_mm >= MODERATE_RAIN_MM:
        return "Mua vua"
    return "Mua nhe"


def check_point(point: dict, forecast_json: dict) -> dict | None:
    """Return an alert dict if this point shows current or imminent rain, else None."""
    current = forecast_json["current"]
    location = forecast_json["location"]
    hours = forecast_json["forecast"]["forecastday"][0]["hour"]

    now = datetime.strptime(location["localtime"], TIME_FMT)

    current_precip = current.get("precip_mm", 0) or 0
    current_condition = current["condition"]["text"]
    if current_precip >= CURRENT_PRECIP_THRESHOLD_MM and not _looks_clear(current_condition):
        return {
            "name": point["name"],
            "lat": point["lat"],
            "lon": point["lon"],
            "kind": "dang mua",
            "level": _current_rain_level(current_precip),
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
                "level": "Sap mua",
                "detail": f"{chance}% kha nang mua luc {hour_label} ({hour['condition']['text']})",
            }

    return None
