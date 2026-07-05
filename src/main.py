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
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    return {}


def save_state(state: dict) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def in_cooldown(state: dict, zone: str, now: datetime) -> bool:
    last = state.get(zone)
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

    if not alerts:
        print("No rain detected this cycle.")
        return

    now = datetime.now()
    state = load_state()
    fresh_alerts = [a for a in alerts if not in_cooldown(state, a["name"], now)]

    if not fresh_alerts:
        print(f"{len(alerts)} alert(s) detected but all zones in cooldown.")
        return

    groups: dict[str, list[str]] = {}
    for a in fresh_alerts:
        groups.setdefault(a["level"], []).append(a["name"])
        state[a["name"]] = now.isoformat()

    rows = [(level, ", ".join(groups[level])) for level in LEVEL_ORDER if level in groups]

    col_width = max(len(level) for level, _ in rows) + 1
    lines = ["<b>Canh bao mua - TP.HCM</b>", "<pre>"]
    for level, names in rows:
        lines.append(f"{level.ljust(col_width)}| {names}")
    lines.append("</pre>")
    send_message(bot_token, chat_id, "\n".join(lines))

    image_path = Path(tempfile.gettempdir()) / "rain_alert.png"
    title = f"Canh bao mua TP.HCM - {now.strftime('%H:%M %d/%m/%Y')}"
    render_table_image(rows, image_path, title=title)
    send_photo(bot_token, chat_id, image_path, caption=f"{len(fresh_alerts)} khu vuc dang/sap mua")

    save_state(state)
    print(f"Sent alert for {len(fresh_alerts)} zone(s).")


if __name__ == "__main__":
    main()
