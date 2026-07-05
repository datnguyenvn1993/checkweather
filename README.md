# Weather Alert HCMC

Phat hien mua som tai TP.HCM bang cach lay mau ngau nhien 24-30 diem toa do
moi 5 phut, goi WeatherAPI.com, va bao qua Telegram khi phat hien mua/sap mua.

## Cau truc

- `src/grid.py` - danh sach diem toa do + ham lay mau ngau nhien
- `src/weather_client.py` - goi WeatherAPI.com forecast endpoint
- `src/detector.py` - nguong phat hien mua hien tai / sap mua (2h toi)
- `src/notifier.py` - gui tin nhan Telegram
- `src/main.py` - dieu phoi toan bo, chong spam theo cooldown 30 phut/khu vuc
- `state/last_alerts.json` - trang thai lan canh bao cuoi cua tung khu vuc (duoc GitHub Actions commit lai)
- `.github/workflows/check_rain.yml` - cron chay moi 5 phut

## Setup

1. Tao repo GitHub (khuyen nghi **public** de khong bi gioi han Actions minutes).
2. Vao repo Settings -> Secrets and variables -> Actions, tao 3 secret:
   - `WEATHERAPI_KEY`
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
3. Push code len repo. Workflow se tu chay moi 5 phut (co the tre vai phut do GitHub Actions khong dam bao dung gio).

## Chay thu local

```bash
pip install -r requirements.txt
cd src
export WEATHERAPI_KEY=...
export TELEGRAM_BOT_TOKEN=...
export TELEGRAM_CHAT_ID=...
python main.py
```

## Tuy chinh nguong

Sua cac hang so trong `src/detector.py`:
- `RAIN_CHANCE_THRESHOLD` (mac dinh 60%)
- `CURRENT_PRECIP_THRESHOLD_MM` (mac dinh 0.1mm)
- `LOOKAHEAD_HOURS` (mac dinh 2 gio toi)

Va cooldown trong `src/main.py` (`COOLDOWN_MINUTES`, mac dinh 30 phut).
