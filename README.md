# Weather Alert HCMC

Phat hien mua som tai TP.HCM bang cach kiem tra 24-25 diem "nong" (mall, khu
vui choi, ben xe, benh vien...) moi 5 phut, goi WeatherAPI.com, va bao qua
Telegram khi phat hien mua/sap mua, hoac khi mot khu vuc het mua.

## Cau truc

- `src/grid.py` - danh sach diem toa do (mall, ben xe, benh vien...) + ham lay mau ngau nhien
- `src/weather_client.py` - goi WeatherAPI.com forecast endpoint
- `src/detector.py` - nguong phat hien mua hien tai / sap mua (2h toi), phan loai muc do (Mua to/vua/nhe/Sap mua)
- `src/notifier.py` - gui tin nhan + anh vao Telegram
- `src/render.py` - ve anh bang (table trong table) theo tung muc do mua
- `src/main.py` - dieu phoi toan bo: chong spam theo cooldown 30 phut/khu vuc, va bao "het mua" khi khu vuc dang mua o chu ky truoc nhung chu ky nay khong con
- `state/last_alerts.json` - cooldown + danh sach khu vuc dang mua o lan chay gan nhat (duoc GitHub Actions commit lai)
- `.github/workflows/check_rain.yml` - cron chay moi 5 phut

## Setup

1. Tao repo GitHub (khuyen nghi **public** de khong bi gioi han Actions minutes).
2. Vao repo Settings -> Secrets and variables -> Actions, tao 3 secret:
   - `WEATHERAPI_KEY`
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
3. Push code len repo. Workflow se tu chay moi 5 phut (co the tre do lich GitHub Actions
   khong dam bao dung gio - xem ghi chu ben duoi).

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
- `HEAVY_RAIN_MM` / `MODERATE_RAIN_MM` - nguong phan loai Mua to / Mua vua / Mua nhe
- `LOOKAHEAD_HOURS` (mac dinh 2 gio toi)

Va cooldown trong `src/main.py` (`COOLDOWN_MINUTES`, mac dinh 30 phut).

## Ghi chu ve do tin cay cua lich chay

GitHub Actions `schedule:` la best-effort, khong dam bao chay dung phut - dac biet
voi repo moi/it hoat dong. Neu thay workflow khong tu chay dieu dan, dung 1 nguon
lich ben ngoai (Google Apps Script time-driven trigger, hoac cron-job.org) de goi
API `workflow_dispatch` cua GitHub moi 5 phut thay vi phu thuoc `schedule:` noi bo.

## Microsoft Teams (dang tam hoan)

Co thu chuyen sang gui canh bao qua Microsoft Teams (webhook Workflows), nhung
gap loi cau hinh "Invalid ThreadId" o action "Post card in a chat or channel"
(chua xac dinh duoc chinh xac nguyen nhan phia Power Automate). Code Adaptive
Card cho Teams van con trong `src/notifier_teams.py` (khong duoc dung trong
`main.py` hien tai) de tiep tuc debug/tich hop sau.
