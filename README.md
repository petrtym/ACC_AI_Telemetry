# ACC Telemetry Client

> Connect Assetto Corsa Competizione to **[@acc_telemetry_bot](https://t.me/acc_telemetry_bot)**

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Windows](https://img.shields.io/badge/Windows-only-0078D6?logo=windows)](https://microsoft.com/windows)
[![Telegram](https://img.shields.io/badge/Bot-@acc__telemetry__bot-2CA5E0?logo=telegram)](https://t.me/acc_telemetry_bot)
[![License: MIT](https://img.shields.io/badge/License-MIT-22c55e)](LICENSE)

Reads telemetry directly from ACC shared memory — no plugins, no mods — and streams it to the bot.
After every lap you get a full report + overlay chart in Telegram.

---

## What you get after every lap

```
🏆 Personal Best!
🏁 Monza

⏱ 1:47.234
🚗 McLaren 720S GT3 Evo  ·  dry_compound

Score:  🟢 ▓▓▓▓▓▓▓▓░░ 83

⚡ Throttle: 68%  🔴 Brake: 24%
💨 Avg: 187.4 km/h  Max: 289.1 km/h
📈 Long G: 1.84g   Lat G: 3.12g
🌡 FL 94° ████░░░░   RR 91° ███░░░░░
⛽ 23.4 L

🤖 Rear slip sits in a good window through Lesmo complex.
   Brake bias 1 click forward would recover ~0.12s at Parabolica —
   you're currently underloading the front axle on entry.
```

Plus an **overlay chart** — throttle / brake / speed / gear, best lap vs last lap.

---

## Features

| Feature | Details |
|---|---|
| 📡 **Live** | Speed, RPM, gear, temps, TC/ABS snapshot on demand |
| ⏱ **Lap report** | Auto-sent after every completed lap |
| 🤖 **AI engineer** | Gemini 1.5 Flash analysis — specific, actionable, F1 pit wall tone |
| 📊 **Overlay chart** | 4-panel throttle/brake/speed/gear — best vs last |
| 🏆 **My Laps** | Personal leaderboard per track + delta chart |
| 🌍 **Global** | Best lap per user on each track — compete with others |
| 📋 **Stats table** | Top 10 laps: date, avg speed, throttle%, tyre temp, score |
| 🏅 **My PBs** | Personal bests across all tracks |
| ⚠️ **Lap validation** | Short laps / pit outlaps auto-filtered |
| 🗺 **Auto track** | Track name read from ACC memory — no manual input |

---

## Setup

### 1. Get your key

Open Telegram → [@acc_telemetry_bot](https://t.me/acc_telemetry_bot) → `/start` → copy the key.

### 2. Install

```cmd
git clone [https://github.com/petrtym/ACC_AI_Telemetry]
cd acc-telemetry-client
pip install requests python-dotenv
```

### 3. Configure

```cmd
copy .env.client.example .env
notepad .env
```

```env
ACC_SERVER_URL=https://acc-telemetry-bot.com   # shown when you /start the bot
ACC_API_KEY=acc_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 4. Drive

1. Launch **Assetto Corsa Competizione**
2. Load any session
3. `python telemetry_client.py`
4. Drive — Telegram message arrives after every lap ✅

---

## Configuration

| Variable | Default | Description |
|---|---|---|
| `ACC_SERVER_URL` | — | **Required** — server URL from the bot |
| `ACC_API_KEY` | — | **Required** — key from `/start` |
| `LIVE_INTERVAL` | `2.0` | Seconds between live telemetry pushes |
| `SAMPLE_INTERVAL` | `0.05` | Trace sampling rate in seconds (0.05 = 20 Hz) |
| `MAX_TRACE_PTS` | `3000` | Max trace points per lap (auto-downsampled) |

---

## How it works

```
ACC shared memory ──▶ telemetry_client.py ──HTTPS──▶ bot server ──▶ Telegram
  (no mods needed)         (your PC)
```

Three memory maps read per tick:

- `acpmf_physics` — speed, gas, brake, G-forces, tyre temps, wheel slip
- `acpmf_graphics` — lap times, sector, TC/ABS, session state
- `acpmf_static` — track name and car model (read once on connect)

Trace sampled at **20 Hz** → ~2,400 points for a 2-minute lap.
Auto-downsampled to `MAX_TRACE_PTS` before upload.

---

## Lap Score  (0 – 100)

```
Score = 50
  + longitudinal G bonus  (up to +32)  — acceleration efficiency
  + lateral G bonus       (up to +23)  — tyre loading in corners
  − rear slip penalty     (up to −45)  — wasted power through wheelspin
```

`🟢 80+`  great traction  ·  `🟡 60–79`  room to improve  ·  `🔴 <60`  significant losses

---

## Lap Validation

Laps shorter than **60 seconds** are automatically marked invalid and not saved.
This filters out pit outlaps, formation laps, and aborted laps.
You'll still get a warning message in Telegram when this happens.

---

## Requirements

- **Windows 10 / 11** (ACC shared memory is Windows-only)
- **Python 3.11+**
- **Assetto Corsa Competizione**
- `pip install requests python-dotenv`

---

## Privacy

- Data is isolated per Telegram account
- Global leaderboard shows your Telegram display name or `@username`
- You see only your own laps — other users' telemetry traces are never exposed
- `/newkey` in the bot invalidates your old key and generates a fresh one

---

## Self-hosting

Don't want to use `@acc_telemetry_bot`? Run your own instance.

`bot_server.py` in this repo is the full server.

```bash
pip install aiogram aiohttp matplotlib python-dotenv
cp .env.server.example .env   # fill BOT_TOKEN, optionally GEMINI_API_KEY
bash install_service.sh       # systemd service on Linux VPS
```

Free Gemini API key: [aistudio.google.com/apikey](https://aistudio.google.com/apikey)

---

## Roadmap

- [ ] `/export` — CSV download for ML / data analysis
- [ ] Micro-sector TC optimisation map
- [ ] Stint mode — fuel and tyre life projections
- [ ] Weather-aware setup delta recommendations

---

MIT License
