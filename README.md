# ACC Telemetry Client

> Connect **Assetto Corsa Competizione** to **[@acc_telemetry_bot](https://t.me/acc_telemetry_bot)** on Telegram.
>
> Your personal AI race engineer — live in your pocket.

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?logo=windows)](https://microsoft.com/windows)
[![Telegram](https://img.shields.io/badge/Bot-@acc__telemetry__bot-2CA5E0?logo=telegram)](https://t.me/acc_telemetry_bot)
[![License: MIT](https://img.shields.io/badge/License-MIT-22c55e)](LICENSE)

Reads telemetry directly from ACC shared memory — **no mods, no plugins, no DLL injection**.
After every lap you get a full debrief, overlay charts, and AI engineer commentary in Telegram.

---

## What you get after every lap

```
🏆 Personal best!
🏁 Spa (track config)

⏱ 2:20.135
🚗 McLaren 720S GT3 Evo  ·  🏎 Dry
Score:  🟡 ▓▓▓▓▓▓▓░░░ 72/100

🎖 Rating:  🔵 D3  (+0.578s vs ref)  →  D2 needs -0.578s
░░░▓▓▓▓░░  D6→Alien

⚡ Throttle 82%  🔴 Brake 5%
💨 Avg 190  Max 267 km/h
📈 G lon 2.14g  lat 3.34g
🌡 FL 78° ███░░░░░  RR 80° ███░░░░░
🟢 TC: 3x   🟢 ABS: 1x
⛽ 10.2 L

📍 Micro-sectors  (+1.237s total)
  🔴 45%  +0.312s
  🔴 20%  +0.187s
  🟢 62%  -0.095s

🤖 Engineer:
• Good throttle pick-up through Raidillon, but braking point at Stavelot
  is 0.8% inconsistent — costing ~0.18s across the stint.
• Rear-left running 6° hotter than FL — reduce TC by 1 on Kemmel exits.
```

Plus an automatic **Throttle / Brake / Speed / Long-G overlay chart** comparing this lap to your best.

---

## Features

### Every lap, automatically
| | Feature |
|---|---|
| ⏱ | Lap time, personal best delta, global leaderboard position |
| 🎖 | Driver rating: D6 → D5 → D4 → D3 → D2 → D1 → Alien (25 tracks) |
| 📊 | Lap score 0–100 based on G-force utilisation and traction |
| 📍 | Micro-sector analysis — where exactly you lose and gain time |
| 🤖 | AI engineer debrief (Gemini) — specific, actionable, 3-4 bullets |
| 📈 | Overlay chart: throttle / brake / speed / long-G vs your best lap |
| ⛔ | Lap validity detection — track limits and tyres off excluded automatically |

### On demand (keyboard buttons)
| Button | What it does |
|---|---|
| 📡 **Live** | Real-time snapshot: speed, RPM, gear, throttle/brake bars, tyre temps, TC/ABS |
| ⏱ **Last Lap** | Full stats of the most recent lap |
| 🏆 **My Laps** | Personal leaderboard per track + bar chart |
| 🌍 **Global** | Global leaderboard — all bot users, best lap per track |
| 📊 **Compare** | Overlay chart: best vs last lap |
| 📍 **Sectors** | Micro-sector delta chart vs your best |
| 📋 **Stats** | Lap table: time, delta, throttle%, avg/max speed, tyre temps, score |
| 🔬 **Analysis** | Consistency score, driving style profile, TC/ABS breakdown, fuel per lap |
| 📈 **Progress** | Long-term progress chart: best per day, all laps, latest stint |
| 🗺 **Map** | Track map coloured by speed delta and brake input |
| 🆚 **vs P1** | Your best lap telemetry vs the global P1 |
| ⛽ **Stint** | Stint planner: laps, fuel needed, tyre deg trend, pit window |
| 🔬 **Corners** | Corner-by-corner analysis: brake point consistency, line consistency |
| ⚙️ **Setup** | Rule-based setup hints from your telemetry data |
| 👻 **Ghost** | Top-5 laps overlaid on one track map |
| ⏱ **∆ Map** | Delta-time track map — where you're gaining/losing vs best |
| 🎖 **Rating** | Driver rating across all your tracks |
| 🎲 **Randomize** | Random training session (track, weather, temp, laps, session type) |
| 👥 **Team** | Team mode — share results with coach/teammates |

### Commands
| Command | Description |
|---|---|
| `/start` | Register and get your API key |
| `/mykey` | Show API key |
| `/newkey` | Regenerate key (old one stops working) |
| `/tracks` | List your tracks with lap count and best times |
| `/fuel <laps>` | Fuel calculator for a specific number of laps |
| `/stint <min>` | Stint planner for a specific duration |
| `/rating` | Full driver rating across all tracks |
| `/corners` | Corner analysis for your latest track |
| `/setup` | Setup hints from telemetry |
| `/ghost` | Ghost overlay for your latest track |
| `/deltamap` | Delta-time map for your latest track |
| `/progress` | Progress chart for your latest track |
| `/vs` | Your best vs global P1 |
| `/random` | Random training session |
| `/team create <name>` | Create a team (you become coach) |
| `/team join <CODE>` | Join a team |
| `/team list` | Your teams |
| `/team board` | Team leaderboard |

---

## Driver Rating

Benchmarked against the ACC community reference times for all 25 tracks:

| Level | Icon | Description |
|---|---|---|
| **Alien** | 👽 | Top 0.1% — faster than most pros |
| **D1** | 🔥 | Very fast amateur / semi-pro level |
| **D2** | 🟣 | Strong club racer |
| **D3** | 🔵 | Competitive intermediate |
| **D4** | 🟡 | Solid intermediate |
| **D5** | 🟠 | Developing |
| **D6** | ⚪️ | Beginner |

After each lap the bot tells you exactly how many seconds you need to cut to reach the next tier.

---

## Setup

### 1. Start the bot → get your API key

Open Telegram → [@acc_telemetry_bot](https://t.me/acc_telemetry_bot) → `/start`

Copy the key shown in the welcome message.

### 2. Install the client

```cmd
git clone https://github.com/YOUR_USERNAME/acc-telemetry-client
cd acc-telemetry-client

pip install requests python-dotenv

copy .env.client.example .env
notepad .env
```

Fill in your `.env`:
```env
ACC_SERVER_URL=https://your-server-address-here
ACC_API_KEY=acc_xxxxxxxxxxxxxxxxxxxx
```

> The server URL is pinned in the [@acc_telemetry_bot](https://t.me/acc_telemetry_bot) channel description.

### 3. Run

```cmd
:: 1. Launch ACC
:: 2. Load a session
:: 3. Run:
python telemetry_client.py
```

Console output:
```
ACC Race Engineer Client
Server : https://...
Key    : acc_1234...
Rate   : 20 Hz  |  min lap pts: 80
Press Ctrl+C to stop.

  ✅  Lap #1 skipped — outlap (pit exit)
  ✅  Lap #2  2:21.372  [Spa (track config)]  (480 pts)
  ✅  Lap #3  2:20.135  [Spa (track config)]  (491 pts)
```

---

## Configuration

All options in your `.env` file:

| Variable | Default | Description |
|---|---|---|
| `ACC_SERVER_URL` | — | **Required.** Server address |
| `ACC_API_KEY` | — | **Required.** Key from `/mykey` in bot |
| `LIVE_INTERVAL` | `2.0` | Seconds between live telemetry updates |
| `SAMPLE_HZ` | `20` | Sampling rate (10–25 recommended) |

---

## How it works

The client reads data directly from **ACC shared memory** — the same interface used by professional tools like MoTeC i2 and Crew Chief.

```
ACC shared memory (acpmf_physics / acpmf_graphics / acpmf_static)
        │
telemetry_client.py  ←  runs on your gaming PC
        │  HTTPS POST  (after every lap + every 2s live)
        ▼
Bot server  →  Telegram
```

**What gets captured per lap point (20 Hz):**
- Lap position (0.0 – 1.0)
- Throttle, brake, steering angle
- Speed, RPM, gear
- Longitudinal and lateral G-force
- Rear wheel slip ratio
- Tyre core temperatures (FL, FR, RL, RR)
- TC and ABS intervention detection
- World XY coordinates (for track maps and ghost overlay)
- Lap timestamp in milliseconds (for delta-time calculations)

**Lap validity:** Outlaps (pit exits) are automatically skipped. Laps where 2+ tyres leave the track for 3+ consecutive frames are marked invalid and excluded from leaderboards.

Data is downsampled to ≤600 points before sending to keep bandwidth minimal.

---

## Privacy

- All data is linked to your Telegram account only via your API key
- No emails, passwords, or third-party logins required
- Global leaderboard shows only your Telegram display name or @username
- Delete your data anytime with `/newkey` (old key and associated data becomes inaccessible)

---

## Troubleshooting

| Error | Fix |
|---|---|
| `ACC_API_KEY not set` | Create `.env` from `.env.client.example` and fill in your key |
| `Server unreachable` | Check `ACC_SERVER_URL` in `.env` and that the bot is online |
| `Could not connect to shared memory` | Launch ACC first, then run the client |
| `Lap skipped — outlap` | Normal — the first lap out of pits is always skipped |
| `Lap skipped — too short` | You started the client mid-lap; next full lap will be recorded |
| Track map / Ghost show no data | You need laps recorded with client v3.0+ (XY data) |

---

## Requirements

- **Windows** PC with Assetto Corsa Competizione installed
- **Python 3.11+**
- Telegram account
- Internet connection from gaming PC to server

```
pip install requests python-dotenv
```

---

## License

MIT — free to use, modify, and distribute.
