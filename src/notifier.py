import requests

TIMEOUT_SECONDS = 10


def send_message(bot_token: str, chat_id: str, text: str) -> None:
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }
    resp = requests.post(url, json=payload, timeout=TIMEOUT_SECONDS)
    resp.raise_for_status()


def send_photo(bot_token: str, chat_id: str, image_path, caption: str = "") -> None:
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    with open(image_path, "rb") as photo_file:
        files = {"photo": photo_file}
        data = {"chat_id": chat_id, "caption": caption}
        resp = requests.post(url, data=data, files=files, timeout=TIMEOUT_SECONDS)
    resp.raise_for_status()
