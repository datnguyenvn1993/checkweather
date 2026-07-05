import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from pathlib import Path

from detector import check_point
from grid import sample_points
from notifier import send_message
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

    lines = ["<b>Canh bao mua - TP.HCM</b>"]
    for a in fresh_alerts:
        lines.append(f"- <b>{a['name']}</b>: {a['detail']}")
        state[a["name"]] = now.isoformat()

    message = "\n".join(lines)
    send_message(bot_token, chat_id, message)
    save_state(state)
    print(f"Sent alert for {len(fresh_alerts)} zone(s).")


if __name__ == "__main__":
    main()
