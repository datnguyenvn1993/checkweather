import json
import os
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from pathlib import Path

from detector import LEVEL_ORDER, check_point
from grid import sample_points
from notifier import send_message, send_photo
from render import render_table_image
from weather_client import get_forecast

STATE_PATH = Path(__file__).resolve().parent.parent / "state" / "last_alerts.json"
COOLDOWN_MINUTES = 30
MAX_WORKERS = 10


def load_state() -> dict:
    if STATE_PATH.exists():
        data = json.loads(STATE_PATH.read_text(encoding="utf-8"))
        if "cooldowns" in data:
            return data
    return {"cooldowns": {}, "last_raining_zones": []}


def save_state(state: dict) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def in_cooldown(cooldowns: dict, zone: str, now: datetime) -> bool:
    last = cooldowns.get(zone)
    if not last:
        return False
    last_time = datetime.fromisoformat(last)
    return now - last_time < timedelta(minutes=COOLDOWN_MINUTES)


def main() -> None:
    api_key = os.environ["WEATHERAPI_KEY"]
    bot_token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]

    points = sample_points()
    print(f"Checking {len(points)} points...")

    alerts = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_point = {
            executor.submit(get_forecast, p["lat"], p["lon"], api_key): p for p in points
        }
        for future in as_completed(future_to_point):
            point = future_to_point[future]
            try:
                forecast_json = future.result()
            except Exception as exc:
                print(f"  [skip] {point['name']}: {exc}", file=sys.stderr)
                continue
            alert = check_point(point, forecast_json)
            if alert:
                alerts.append(alert)

    now = datetime.now()
    state = load_state()
    cooldowns = state["cooldowns"]

    current_alert_by_zone = {a["name"]: a for a in alerts}
    current_raining_zones = set(current_alert_by_zone)
    previous_raining_zones = set(state.get("last_raining_zones", []))
    stopped_zones = sorted(previous_raining_zones - current_raining_zones)

    fresh_alerts = [a for a in current_alert_by_zone.values() if not in_cooldown(cooldowns, a["name"], now)]

    if fresh_alerts:
        groups: dict[str, list[str]] = {}
        for a in fresh_alerts:
            groups.setdefault(a["level"], []).append(a["name"])
            cooldowns[a["name"]] = now.isoformat()

        rows = [(level, groups[level]) for level in LEVEL_ORDER if level in groups]

        col_width = max(len(level) for level, _ in rows) + 1
        lines = ["<b>Canh bao mua - TP.HCM</b>", "<pre>"]
        for level, names in rows:
            lines.append(f"{level.ljust(col_width)}| {', '.join(names)}")
        lines.append("</pre>")
        send_message(bot_token, chat_id, "\n".join(lines))

        image_path = Path(tempfile.gettempdir()) / "rain_alert.png"
        title = f"Canh bao mua TP.HCM - {now.strftime('%H:%M %d/%m/%Y')}"
        render_table_image(rows, image_path, title=title)
        send_photo(bot_token, chat_id, image_path, caption=f"{len(fresh_alerts)} khu vuc dang/sap mua")
        print(f"Sent alert for {len(fresh_alerts)} zone(s).")
    else:
        print(f"{len(alerts)} alert(s) detected but all zones in cooldown or no rain.")

    if stopped_zones:
        send_message(bot_token, chat_id, "<b>Da het mua:</b> " + ", ".join(stopped_zones))
        for zone in stopped_zones:
            cooldowns.pop(zone, None)
        print(f"Rain stopped at {len(stopped_zones)} zone(s).")

    state["last_raining_zones"] = sorted(current_raining_zones)
    save_state(state)


if __name__ == "__main__":
    main()
