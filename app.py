# ═══════════════════════════════════════════════════════════════
# app.py — AGS COMMUNITY · Friend Request Sender API
# Dev: @ags_atif | TG: https://t.me/ags_community
# Endpoint: /send?uid=XXX&password=YYY&target=ZZZ
# ═══════════════════════════════════════════════════════════════

import os
import asyncio
import time

import aiohttp
from flask import Flask, request, jsonify
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

import login_engine
from byte import Encrypt_ID

# ─── Config ───
PORT       = int(os.environ.get("PORT", 10000))
REGION     = os.environ.get("REGION", "IND")
CREDIT     = "sk_community"
DEVELOPER  = "khushi"
VERSION    = "1.0.0"

app = Flask(__name__)

# ─── AES keys (RequestAddingFriend API) ───
_AES_KEY = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
_AES_IV  = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])

_FRIEND_URL = "https://loginbp.ppmainecoonghj.com/RequestAddingFriend"

_HEADERS = {
    'User-Agent': 'UnityPlayer/2018.4.12f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)',
    'Connection': 'Keep-Alive', 'Accept-Encoding': 'gzip',
    'Content-Type': 'application/x-www-form-urlencoded',
    'X-Unity-Version': '2018.4.12f1', 'X-GA-SV': '1789535859',
    'X-GA': 'v1 1', 'ReleaseVersion': 'OB55'
}


# ═══════════════════════════════════════════════════════════════
# Helper — standard response envelope
# ═══════════════════════════════════════════════════════════════
def make_response(success: bool, **extra) -> dict:
    base = {
        "success":    success,
        "credit":     CREDIT,
        "developer":  DEVELOPER,
        "version":    VERSION,
        "timestamp":  int(time.time()),
    }
    base.update(extra)
    return base


# ═══════════════════════════════════════════════════════════════
# Core: Send Friend Request
# ═══════════════════════════════════════════════════════════════
async def send_friend_request(target_uid: str, token: str) -> tuple[bool, str, int | None]:
    """
    Returns (success, message, status_code)
    """
    try:
        encrypted_id = Encrypt_ID(target_uid)
        payload      = f"08a7c4839f1e{encrypted_id}1801"

        cipher      = AES.new(_AES_KEY, AES.MODE_CBC, _AES_IV)
        enc_payload = cipher.encrypt(pad(bytes.fromhex(payload), AES.block_size))

        headers = {**_HEADERS, "Authorization": f"Bearer {token}"}

        async with aiohttp.ClientSession() as session:
            async with session.post(
                _FRIEND_URL,
                headers=headers,
                data=enc_payload,
                ssl=False,
                timeout=aiohttp.ClientTimeout(total=15),
            ) as r:
                if r.status == 200:
                    return True, "Friend request sent successfully", 200
                if r.status == 400:
                    body = await r.text()
                    return False, f"Bad request (400): {body[:180]}", 400
                if r.status == 401:
                    return False, "Unauthorized (401) — token invalid/expired", 401
                if r.status == 429:
                    return False, "Rate limited (429) — try again later", 429
                return False, f"HTTP {r.status}", r.status

    except asyncio.TimeoutError:
        return False, "Request timeout to Garena", 504
    except Exception as e:
        return False, f"Exception: {str(e)}", 500


# ═══════════════════════════════════════════════════════════════
# Async worker (login + send)
# ═══════════════════════════════════════════════════════════════
async def _run(uid: str, password: str, target: str) -> dict:
    t0 = time.time()

    # 1) Login
    try:
        login = await login_engine.do_login(uid, password, REGION)
    except Exception as e:
        return make_response(
            False,
            error=f"Login exception: {e}",
            elapsed_ms=int((time.time() - t0) * 1000),
        )

    if not login:
        return make_response(
            False,
            error="Login failed — check UID / password",
            elapsed_ms=int((time.time() - t0) * 1000),
        )

    bot_name = login.get("account_name", "Unknown")
    token    = login["token"]

    # 2) Send friend request
    ok, msg, code = await send_friend_request(target, token)

    return make_response(
        ok,
        message     = msg if ok else None,
        error       = None if ok else msg,
        bot_uid     = login["bot_uid"],
        bot_name    = bot_name,
        region      = login.get("region", REGION),
        target_uid  = target,
        status_code = code,
        elapsed_ms  = int((time.time() - t0) * 1000),
    )


# ═══════════════════════════════════════════════════════════════
# Routes
# ═══════════════════════════════════════════════════════════════
@app.route("/send", methods=["GET", "POST"])
def send():
    """
    GET  /send?uid=...&password=...&target=...
    POST /send   JSON: {"uid":"...","password":"...","target":"..."}
    """
    if request.method == "POST" and request.is_json:
        data = request.get_json() or {}
        uid      = str(data.get("uid", "")).strip()
        password = str(data.get("password", "")).strip()
        target   = str(data.get("target", "")).strip()
    else:
        uid      = request.args.get("uid", "").strip()
        password = request.args.get("password", "").strip()
        target   = request.args.get("target", "").strip()

    missing = [k for k, v in {"uid": uid, "password": password, "target": target}.items() if not v]
    if missing:
        return jsonify(make_response(
            False,
            error=f"Missing parameter(s): {', '.join(missing)}",
        )), 400

    if not target.isdigit():
        return jsonify(make_response(False, error="target must be a numeric UID")), 400

    try:
        result = asyncio.run(_run(uid, password, target))
        return jsonify(result)
    except Exception as e:
        return jsonify(make_response(False, error=f"Server error: {e}")), 500


@app.route("/")
def home():
    return jsonify({
        "service":    "Friend Request Sender API",
        "credit":     CREDIT,
        "developer":  DEVELOPER,
        "version":    VERSION,
        "endpoint":   "/send",
        "params":     ["uid", "password", "target"],
        "example":    "/send?uid=YOUR_UID&password=YOUR_PW&target=TARGET_UID",
        "method":     "GET or POST (JSON)",
        "status":     "online",
    })


@app.route("/healthz")
def healthz():
    return jsonify({"status": "ok", "credit": CREDIT, "developer": DEVELOPER}), 200


# ═══════════════════════════════════════════════════════════════
# Entry
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print(f"[*] SK Friend Request API on 0.0.0.0:{PORT} | Dev: {DEVELOPER}")
    app.run(host="0.0.0.0", port=PORT, use_reloader=False, threaded=True)