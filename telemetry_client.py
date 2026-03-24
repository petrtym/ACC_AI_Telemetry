import ctypes, json, mmap, os, time
from collections import defaultdict
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

SERVER_URL     = os.getenv("ACC_SERVER_URL",  "http://localhost:8765")
API_KEY        = os.getenv("ACC_API_KEY",     "")
LIVE_INTERVAL  = float(os.getenv("LIVE_INTERVAL", "2.0"))
SAMPLE_HZ      = float(os.getenv("SAMPLE_HZ",    "20"))   # 20 samples/sec
TIMEOUT        = 5

if not API_KEY:
    print("ACC_API_KEY not set!\nGet it from the bot with /mykey and put it in .env")
    exit(1)

SLEEP = 1.0 / SAMPLE_HZ

# ═══════════════════════════════════════════════════════
# ACC SHARED MEMORY STRUCTURES
# ═══════════════════════════════════════════════════════
class SPageFilePhysics(ctypes.Structure):
    _pack_ = 4
    _fields_ = [
        ("packetId",            ctypes.c_int32),
        ("gas",                 ctypes.c_float),
        ("brake",               ctypes.c_float),
        ("fuel",                ctypes.c_float),
        ("gear",                ctypes.c_int32),
        ("rpms",                ctypes.c_int32),
        ("steerAngle",          ctypes.c_float),
        ("speedKmh",            ctypes.c_float),
        ("velocity",            ctypes.c_float * 3),
        ("accG",                ctypes.c_float * 3),
        ("wheelSlip",           ctypes.c_float * 4),
        ("wheelLoad",           ctypes.c_float * 4),
        ("wheelsPressure",      ctypes.c_float * 4),
        ("wheelAngularSpeed",   ctypes.c_float * 4),
        ("tyreWear",            ctypes.c_float * 4),
        ("tyreDirtyLevel",      ctypes.c_float * 4),
        ("tyreCoreTemperature", ctypes.c_float * 4),
        ("camberRAD",           ctypes.c_float * 4),
        ("suspensionTravel",    ctypes.c_float * 4),
        ("drs",                 ctypes.c_float),
        ("tc",                  ctypes.c_float),
        ("heading",             ctypes.c_float),
        ("pitch",               ctypes.c_float),
        ("roll",                ctypes.c_float),
        ("cgHeight",            ctypes.c_float),
        ("carDamage",           ctypes.c_float * 5),
        ("numberOfTyresOut",    ctypes.c_int32),
        ("pitLimiterOn",        ctypes.c_int32),
        ("abs",                 ctypes.c_float),
    ]

class SPageFileGraphic(ctypes.Structure):
    _pack_ = 4
    _fields_ = [
        ("packetId",              ctypes.c_int32),
        ("status",                ctypes.c_int32),
        ("session",               ctypes.c_int32),
        ("currentTime",           ctypes.c_wchar * 15),
        ("lastTime",              ctypes.c_wchar * 15),
        ("bestTime",              ctypes.c_wchar * 15),
        ("split",                 ctypes.c_wchar * 15),
        ("completedLaps",         ctypes.c_int32),
        ("position",              ctypes.c_int32),
        ("iCurrentTime",          ctypes.c_int32),
        ("iLastTime",             ctypes.c_int32),
        ("iBestTime",             ctypes.c_int32),
        ("sessionTimeLeft",       ctypes.c_float),
        ("distanceTraveled",      ctypes.c_float),
        ("isInPit",               ctypes.c_int32),
        ("currentSectorIndex",    ctypes.c_int32),
        ("lastSectorTime",        ctypes.c_int32),
        ("numberOfLaps",          ctypes.c_int32),
        ("tyreCompound",          ctypes.c_wchar * 33),
        ("replayTimeMultiplier",  ctypes.c_float),
        ("normalizedCarPosition", ctypes.c_float),
        ("activeCars",            ctypes.c_int32),
        ("carCoordinates",        ctypes.c_float * 60 * 3),
        ("carID",                 ctypes.c_int32 * 60),
        ("playerCarID",           ctypes.c_int32),
        ("penaltyTime",           ctypes.c_float),
        ("flag",                  ctypes.c_int32),
        ("penalty",               ctypes.c_int32),
        ("idealLineOn",           ctypes.c_int32),
        ("isInPitLane",           ctypes.c_int32),
        ("surfaceGrip",           ctypes.c_int32),
        ("mandatoryPitDone",      ctypes.c_int32),
        ("windSpeed",             ctypes.c_float),
        ("windDirection",         ctypes.c_float),
        ("isSetupMenuVisible",    ctypes.c_int32),
        ("mainDisplayIndex",      ctypes.c_int32),
        ("secondaryDisplayIndex", ctypes.c_int32),
        ("TC",                    ctypes.c_int32),
        ("TCCut",                 ctypes.c_int32),
        ("EngineMap",             ctypes.c_int32),
        ("ABS",                   ctypes.c_int32),
    ]

class SPageFileStatic(ctypes.Structure):
    _pack_ = 4
    _fields_ = [
        ("smVersion",                ctypes.c_wchar * 15),
        ("acVersion",                ctypes.c_wchar * 15),
        ("numberOfSessions",         ctypes.c_int32),
        ("numCars",                  ctypes.c_int32),
        ("carModel",                 ctypes.c_wchar * 33),
        ("track",                    ctypes.c_wchar * 33),
        ("playerName",               ctypes.c_wchar * 33),
        ("playerSurname",            ctypes.c_wchar * 33),
        ("playerNick",               ctypes.c_wchar * 33),
        ("sectorCount",              ctypes.c_int32),
        ("maxTorque",                ctypes.c_float),
        ("maxPower",                 ctypes.c_float),
        ("maxRpm",                   ctypes.c_int32),
        ("maxFuel",                  ctypes.c_float),
        ("suspensionMaxTravel",      ctypes.c_float * 4),
        ("tyreRadius",               ctypes.c_float * 4),
        ("maxTurboBoost",            ctypes.c_float),
        ("deprecated_1",             ctypes.c_float),
        ("deprecated_2",             ctypes.c_float),
        ("penaltiesEnabled",         ctypes.c_int32),
        ("aidFuelRate",              ctypes.c_float),
        ("aidTireRate",              ctypes.c_float),
        ("aidMechanicalDamage",      ctypes.c_float),
        ("aidAllowTyreBlankets",     ctypes.c_int32),
        ("aidStability",             ctypes.c_float),
        ("aidAutoClutch",            ctypes.c_int32),
        ("aidAutoBlip",              ctypes.c_int32),
        ("hasDRS",                   ctypes.c_int32),
        ("hasERS",                   ctypes.c_int32),
        ("hasKERS",                  ctypes.c_int32),
        ("kersMaxJ",                 ctypes.c_float),
        ("engineBrakeSettingsCount", ctypes.c_int32),
        ("ersPowerControllerCount",  ctypes.c_int32),
        ("trackSplineLength",        ctypes.c_float),
        ("trackConfiguration",       ctypes.c_wchar * 33),
        ("ersMaxJ",                  ctypes.c_float),
        ("isTimedRace",              ctypes.c_int32),
        ("hasExtraLap",              ctypes.c_int32),
        ("carSkin",                  ctypes.c_wchar * 33),
        ("reversedGridPositions",    ctypes.c_int32),
        ("PitWindowStart",           ctypes.c_int32),
        ("PitWindowEnd",             ctypes.c_int32),
    ]

# ═══════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════
def ms_to_str(ms):
    if ms <= 0: return "--:--.---"
    m, s = divmod(ms // 1000, 60)
    return f"{m}:{s:02d}.{ms % 1000:03d}"

def format_track(raw, cfg):
    t = raw.strip().replace("_"," ").title() if raw.strip() else "Unknown"
    c = cfg.strip()
    if c and c.lower() not in ("","none",raw.strip().lower()):
        t += f" ({c})"
    return t

def send(endpoint, payload, silent=False):
    try:
        payload["api_key"] = API_KEY
        r = requests.post(f"{SERVER_URL}{endpoint}", json=payload, timeout=TIMEOUT)
        if r.status_code == 401:
            print("Invalid API key! Check .env -> ACC_API_KEY"); return False
        if not silent and r.status_code != 200:
            print(f"[WARN] {endpoint} -> HTTP {r.status_code}")
        return r.status_code == 200
    except requests.exceptions.ConnectionError:
        if not silent: print(f"[WARN] Server unreachable ({SERVER_URL})")
        return False
    except Exception as e:
        if not silent: print(f"[WARN] {e}")
        return False

def avg(lst): return sum(lst)/len(lst) if lst else 0.0

# ═══════════════════════════════════════════════════════
# MAIN LOOP
# ═══════════════════════════════════════════════════════
def main():
    try:
        shm_phys   = mmap.mmap(-1, ctypes.sizeof(SPageFilePhysics),  "Local\\acpmf_physics")
        shm_gfx    = mmap.mmap(-1, ctypes.sizeof(SPageFileGraphic),  "Local\\acpmf_graphics")
        shm_static = mmap.mmap(-1, ctypes.sizeof(SPageFileStatic),   "Local\\acpmf_static")
    except Exception:
        print("Could not connect to ACC shared memory.\nMake sure ACC is running first!")
        return

    print(f"ACC Race Engineer Client")
    print(f"Server : {SERVER_URL}")
    print(f"Key    : {API_KEY[:8]}…")
    print(f"Rate   : {SAMPLE_HZ:.0f} Hz")
    print("Press Ctrl+C to stop.\n")

    if not send("/health", {}, silent=True):
        print("⚠ Server not reachable — laps will be lost if connection stays down\n")

    prev_laps      = -1
    last_live_send = 0.0
    # Lap validity tracking
    lap_had_tyres_out = False

    cur_trace: list  = []
    cur_stats        = defaultdict(list)

    while True:
        try:
            p  = SPageFilePhysics.from_buffer_copy(shm_phys)
            g  = SPageFileGraphic.from_buffer_copy(shm_gfx)
            st = SPageFileStatic.from_buffer_copy(shm_static)

            track     = format_track(st.track, st.trackConfiguration)
            car_model = st.carModel.strip().replace("_"," ").title() or "Unknown"
            speed     = p.speedKmh
            comp_laps = g.completedLaps
            tyres_out = p.numberOfTyresOut

            # Track validity: if any lap point had tyres off, mark invalid
            if tyres_out > 0 and speed > 5:
                lap_had_tyres_out = True

            # ── Lap finished ──────────────────────────────────────────────
            lap_finished = (prev_laps >= 0 and comp_laps > prev_laps and g.iLastTime > 0)
            if lap_finished:
                is_valid = int(not lap_had_tyres_out and g.iLastTime < 600_000)
                # Downsample trace to max 500 points for bandwidth
                trace = cur_trace
                if len(trace) > 500:
                    step  = len(trace) // 500
                    trace = trace[::step]

                stats = {
                    "avg_throttle": round(avg(cur_stats["throttle"]), 4),
                    "avg_brake":    round(avg(cur_stats["brake"]),    4),
                    "avg_speed":    round(avg(cur_stats["speed"]),    2),
                    "max_speed":    round(max(cur_stats["speed"], default=0), 1),
                    "avg_slip_rr":  round(avg(cur_stats["slip_rr"]), 5),
                    "max_g_lon":    round(max(cur_stats["g_lon"],  default=0), 3),
                    "max_g_lat":    round(max(cur_stats["g_lat"],  default=0), 3),
                    "avg_tyre_fl":  round(avg(cur_stats["tyre_fl"]), 1),
                    "avg_tyre_rr":  round(avg(cur_stats["tyre_rr"]), 1),
                    "avg_fuel":     round(avg(cur_stats["fuel"]),    2),
                }
                payload = {
                    "lap_number":   comp_laps,
                    "lap_time_ms":  g.iLastTime,
                    "lap_time_str": ms_to_str(g.iLastTime),
                    "track":        track,
                    "car":          car_model,
                    "compound":     g.tyreCompound.strip(),
                    "is_valid":     is_valid,
                    "trace":        trace,
                    **stats,
                }
                ok = send("/lap", payload)
                v_tag = "" if is_valid else " [INVALID]"
                icon  = "✅" if ok else "⚠ (no connection)"
                print(f"  {icon}  Lap #{comp_laps}  {ms_to_str(g.iLastTime)}{v_tag}"
                      f"  [{track}]  ({len(trace)} pts)")
                cur_trace = []
                cur_stats = defaultdict(list)
                lap_had_tyres_out = False

            prev_laps = comp_laps

            # ── Buffer ────────────────────────────────────────────────────
            if speed > 5.0:
                cur_trace.append({
                    "pos":      round(g.normalizedCarPosition, 4),
                    "throttle": round(p.gas,      3),
                    "brake":    round(p.brake,     3),
                    "speed":    round(speed,        1),
                    "g_lon":    round(p.accG[2],   3),
                    "g_lat":    round(p.accG[0],   3),
                    "slip_rr":  round(p.wheelSlip[3], 4),
                    "tc":       g.TC,
                })
                cur_stats["throttle"].append(p.gas)
                cur_stats["brake"].append(p.brake)
                cur_stats["speed"].append(speed)
                cur_stats["slip_rr"].append(p.wheelSlip[3])
                cur_stats["g_lon"].append(abs(p.accG[2]))
                cur_stats["g_lat"].append(abs(p.accG[0]))
                cur_stats["tyre_fl"].append(p.tyreCoreTemperature[0])
                cur_stats["tyre_rr"].append(p.tyreCoreTemperature[3])
                cur_stats["fuel"].append(p.fuel)

            # ── Live ──────────────────────────────────────────────────────
            now = time.time()
            if now - last_live_send >= LIVE_INTERVAL:
                send("/live", {
                    "speed":     round(speed, 1),
                    "rpm":       p.rpms,
                    "gear":      p.gear - 1,
                    "gas":       round(p.gas,   2),
                    "brake":     round(p.brake, 2),
                    "tc":        g.TC,
                    "abs":       g.ABS,
                    "lap_pos":   round(g.normalizedCarPosition, 4),
                    "lap_time":  g.currentTime.strip(),
                    "best_time": g.bestTime.strip(),
                    "comp_laps": comp_laps,
                    "fuel":      round(p.fuel, 2),
                    "tyre_fl":   round(p.tyreCoreTemperature[0], 1),
                    "tyre_fr":   round(p.tyreCoreTemperature[1], 1),
                    "tyre_rl":   round(p.tyreCoreTemperature[2], 1),
                    "tyre_rr":   round(p.tyreCoreTemperature[3], 1),
                    "slip_rr":   round(p.wheelSlip[3], 4),
                    "in_pit":    bool(g.isInPit or g.isInPitLane),
                    "sector":    g.currentSectorIndex + 1,
                    "track":     track,
                    "car":       car_model,
                }, silent=True)
                last_live_send = now

            time.sleep(SLEEP)

        except KeyboardInterrupt:
            print("\nClient stopped.")
            break
        except Exception as e:
            print(f"[ERR] {e}")
            time.sleep(0.5)

if __name__ == "__main__":
    main()