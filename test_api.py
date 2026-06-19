#!/usr/bin/env python3
"""
Test script for Nahman AI API.
Run with: python test_api.py
Requires the server to be running on http://localhost:8000
"""

import sys
import requests

BASE = "http://localhost:8000"
PASS = "\033[92m✓\033[0m"
FAIL = "\033[91m✗\033[0m"
failures = 0


def check(label, condition, detail=""):
    global failures
    if condition:
        print(f"  {PASS} {label}")
    else:
        print(f"  {FAIL} {label}{' — ' + detail if detail else ''}")
        failures += 1


def section(title):
    print(f"\n{title}")
    print("─" * 40)


# ── Health & Info ─────────────────────────────────────────────────────────────

section("1. Health & Info")

r = requests.get(f"{BASE}/api/health")
check("GET /api/health → 200", r.status_code == 200)
check("returns status=ok", r.json().get("status") == "ok")

r = requests.get(f"{BASE}/api")
check("GET /api → 200", r.status_code == 200)
check("returns nom=Nahman AI", r.json().get("nom") == "Nahman AI")

r = requests.get(f"{BASE}/api/aide")
check("GET /api/aide → 200", r.status_code == 200)
check("has 'description' key", "description" in r.json())

# ── Static files ──────────────────────────────────────────────────────────────

section("2. Static files (frontend)")

r = requests.get(f"{BASE}/")
check("GET / → 200 (index.html)", r.status_code == 200)
check("Content-Type is HTML", "text/html" in r.headers.get("content-type", ""))

r = requests.get(f"{BASE}/chat.html")
check("GET /chat.html → 200", r.status_code == 200)
check("Contains 'Nahman AI'", "Nahman AI" in r.text)

# ── Chat endpoint ─────────────────────────────────────────────────────────────

section("3. POST /api/chat")

r = requests.post(f"{BASE}/api/chat", json={"texte": "Dis juste 'OK' en un mot."})
check("POST /api/chat → 200", r.status_code == 200)
check("has 'message' key", "message" in r.json(), str(r.json()))
check("message is non-empty", len(r.json().get("message", "")) > 0)

r = requests.post(f"{BASE}/api/chat", json={"texte": ""})
check("POST /api/chat empty → handled", r.status_code == 200)
check("returns helpful message", len(r.json().get("message", "")) > 0)

r = requests.post(
    f"{BASE}/api/chat",
    json={"texte": "Reply with just the word PONG", "system_prompt": "Always reply with just the word PONG."}
)
check("POST /api/chat with system_prompt → 200", r.status_code == 200)
check("custom system_prompt accepted", "message" in r.json())

# ── Config endpoints ──────────────────────────────────────────────────────────

section("4. Config endpoints")

r = requests.get(f"{BASE}/api/config/prompt")
check("GET /api/config/prompt → 200", r.status_code == 200)
check("has 'prompt_actuel' key", "prompt_actuel" in r.json())

r = requests.post(f"{BASE}/api/config/prompt", json={"prompt": "Tu es un robot très formel."})
check("POST /api/config/prompt → 200", r.status_code == 200)
check("prompt updated", "mis à jour" in r.json().get("message", ""))

r = requests.post(f"{BASE}/api/config/prompt/reset")
check("POST /api/config/prompt/reset → 200", r.status_code == 200)
check("prompt reset", "réinitialisé" in r.json().get("message", ""))

# ── Summary ───────────────────────────────────────────────────────────────────

total = 20
passed = total - failures
print(f"\n{'─' * 40}")
if failures == 0:
    print(f"\033[92m✓ All {total} tests passed!\033[0m")
else:
    print(f"\033[91m{failures}/{total} tests failed.\033[0m")
    sys.exit(1)
