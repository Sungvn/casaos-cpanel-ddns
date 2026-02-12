import json
import os
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
from flask import Flask, jsonify, request, send_from_directory
from waitress import serve

APP_PORT = int(os.getenv("PORT", "7788"))
CONFIG_DIR = Path("/config")
SETTINGS_FILE = CONFIG_DIR / "settings.json"
STATE_FILE = CONFIG_DIR / "state.json"

DEFAULT_WEBCALL_URL = os.getenv("DEFAULT_WEBCALL_URL", "").strip()
DEFAULT_CHECK_INTERVAL = int(os.getenv("DEFAULT_CHECK_INTERVAL", "300"))
DEFAULT_IP_CHECK_URL = os.getenv("DEFAULT_IP_CHECK_URL", "https://api.ipify.org").strip()
TZ = os.getenv("TZ", "UTC")

CONFIG_DIR.mkdir(parents=True, exist_ok=True)

app = Flask(__name__, static_folder="static")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path, default: dict) -> dict:
    try:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        pass
    return default


def save_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def default_settings() -> dict:
    return {
        "webcall_url": DEFAULT_WEBCALL_URL,
        "check_interval": DEFAULT_CHECK_INTERVAL,
        "ip_check_url": DEFAULT_IP_CHECK_URL,
        "enabled": True,
        "last_saved": now_iso(),
    }


def default_state() -> dict:
    return {
        "current_ip": "",
        "last_ip": "",
        "last_update_at": "",
        "last_result": "",
        "last_http_status": None,
        "last_error": "",
        "last_checked_at": "",
    }


settings = load_json(SETTINGS_FILE, default_settings())
state = load_json(STATE_FILE, default_state())

settings_lock = threading.Lock()
state_lock = threading.Lock()


def get_public_ip(ip_check_url: str) -> str:
    r = requests.get(ip_check_url, timeout=10)
    r.raise_for_status()
    return r.text.strip()


def call_webcall(webcall_url: str) -> tuple[str, int]:
    # cPanel webcall URL typically returns simple text; we store a short snippet
    r = requests.get(webcall_url, timeout=15)
    snippet = (r.text or "").strip()
    if len(snippet) > 300:
        snippet = snippet[:300] + "..."
    return snippet, r.status_code


def worker_loop():
    global settings, state
    while True:
        try:
            with settings_lock:
                s = dict(settings)

            if not s.get("enabled", True):
                time.sleep(2)
                continue

            webcall_url = (s.get("webcall_url") or "").strip()
            ip_check_url = (s.get("ip_check_url") or DEFAULT_IP_CHECK_URL).strip()
            interval = int(s.get("check_interval") or DEFAULT_CHECK_INTERVAL)
            if interval < 30:
                interval = 30

            with state_lock:
                state["last_checked_at"] = now_iso()
                save_json(STATE_FILE, state)

            ip = ""
            try:
                ip = get_public_ip(ip_check_url)
            except Exception as e:
                with state_lock:
                    state["last_error"] = f"IP check failed: {e}"
                    save_json(STATE_FILE, state)
                time.sleep(interval)
                continue

            do_update = False
            with state_lock:
                state["current_ip"] = ip
                last_ip = state.get("last_ip", "")
                if ip and ip != last_ip:
                    do_update = True
                save_json(STATE_FILE, state)

            if do_update:
                if not webcall_url:
                    with state_lock:
                        state["last_result"] = "Skipped update: webcall_url not set"
                        state["last_error"] = ""
                        state["last_http_status"] = None
                        save_json(STATE_FILE, state)
                else:
                    try:
                        result_text, http_status = call_webcall(webcall_url)
                        with state_lock:
                            state["last_ip"] = ip
                            state["last_update_at"] = now_iso()
                            state["last_result"] = result_text or "OK"
                            state["last_http_status"] = http_status
                            state["last_error"] = ""
                            save_json(STATE_FILE, state)
                    except Exception as e:
                        with state_lock:
                            state["last_error"] = f"Webcall failed: {e}"
                            save_json(STATE_FILE, state)

            time.sleep(interval)

        except Exception as e:
            with state_lock:
                state["last_error"] = f"Worker error: {e}"
                save_json(STATE_FILE, state)
            time.sleep(10)


@app.get("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.get("/api/status")
def api_status():
    with settings_lock:
        s = dict(settings)
    with state_lock:
        st = dict(state)

    # Never fully expose webcall URL; show only beginning/end
    w = (s.get("webcall_url") or "").strip()
    masked = ""
    if w:
        if len(w) <= 20:
            masked = w
        else:
            masked = w[:12] + "..." + w[-8:]

    return jsonify(
        {
            "settings": {
                "webcall_url_masked": masked,
                "check_interval": s.get("check_interval"),
                "ip_check_url": s.get("ip_check_url"),
                "enabled": s.get("enabled", True),
                "last_saved": s.get("last_saved", ""),
            },
            "state": st,
        }
    )


@app.post("/api/settings")
def api_save_settings():
    data = request.get_json(force=True, silent=False)

    webcall_url = str(data.get("webcall_url", "")).strip()
    ip_check_url = str(data.get("ip_check_url", DEFAULT_IP_CHECK_URL)).strip()
    enabled = bool(data.get("enabled", True))

    try:
        check_interval = int(data.get("check_interval", DEFAULT_CHECK_INTERVAL))
    except Exception:
        check_interval = DEFAULT_CHECK_INTERVAL
    if check_interval < 30:
        check_interval = 30

    new_settings = {
        "webcall_url": webcall_url,
        "check_interval": check_interval,
        "ip_check_url": ip_check_url,
        "enabled": enabled,
        "last_saved": now_iso(),
    }

    with settings_lock:
        global settings
        settings = new_settings
        save_json(SETTINGS_FILE, settings)

    return jsonify({"ok": True, "settings": new_settings})


@app.post("/api/test")
def api_test():
    with settings_lock:
        s = dict(settings)

    webcall_url = (s.get("webcall_url") or "").strip()
    ip_check_url = (s.get("ip_check_url") or DEFAULT_IP_CHECK_URL).strip()

    if not webcall_url:
        return jsonify({"ok": False, "error": "webcall_url is not set"}), 400

    try:
        ip = get_public_ip(ip_check_url)
    except Exception as e:
        return jsonify({"ok": False, "error": f"IP check failed: {e}"}), 500

    try:
        result_text, http_status = call_webcall(webcall_url)
    except Exception as e:
        with state_lock:
            state["last_error"] = f"Test webcall failed: {e}"
            save_json(STATE_FILE, state)
        return jsonify({"ok": False, "error": f"Webcall failed: {e}"}), 500

    with state_lock:
        state["current_ip"] = ip
        state["last_ip"] = ip
        state["last_update_at"] = now_iso()
        state["last_result"] = result_text or "OK"
        state["last_http_status"] = http_status
        state["last_error"] = ""
        save_json(STATE_FILE, state)

    return jsonify({"ok": True, "ip": ip, "http_status": http_status, "result": result_text})


def start_worker():
    t = threading.Thread(target=worker_loop, daemon=True)
    t.start()


if __name__ == "__main__":
    start_worker()
    serve(app, host="0.0.0.0", port=APP_PORT, threads=6)
