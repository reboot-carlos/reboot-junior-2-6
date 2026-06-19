#!/usr/bin/env bash
# Run the full test suite against a running server (default: localhost:8000)
set -euo pipefail

BASE="${1:-http://localhost:8000}"
PASS="\033[92m✓\033[0m"
FAIL="\033[91m✗\033[0m"
failures=0

check() {
  local label="$1"
  local result="$2"
  if [ "$result" = "0" ]; then
    echo -e "  ${PASS} ${label}"
  else
    echo -e "  ${FAIL} ${label}"
    failures=$((failures + 1))
  fi
}

section() { echo -e "\n$1\n$(printf '─%.0s' {1..40})"; }

# ── wait for server ────────────────────────────────────────────────────────────
echo "Waiting for server at ${BASE} ..."
for i in $(seq 1 15); do
  if curl -sf "${BASE}/api/health" > /dev/null 2>&1; then
    echo "Server is up."
    break
  fi
  if [ "$i" -eq 15 ]; then
    echo -e "${FAIL} Server did not respond after 15s. Is it running?"
    exit 1
  fi
  sleep 1
done

# ── helpers ────────────────────────────────────────────────────────────────────
get()  { curl -sf "${BASE}${1}"; }
post() { curl -sf -X POST "${BASE}${1}" -H "Content-Type: application/json" -d "${2}"; }
status() { curl -so /dev/null -w "%{http_code}" "${BASE}${1}"; }
post_status() { curl -so /dev/null -w "%{http_code}" -X POST "${BASE}${1}" -H "Content-Type: application/json" -d "${2}"; }

# ── 1. Health & Info ───────────────────────────────────────────────────────────
section "1. Health & Info"

code=$(status "/api/health"); check "GET /api/health → 200"    "$([ "$code" = "200" ] && echo 0 || echo 1)"
body=$(get "/api/health");    check "returns status=ok"         "$(echo "$body" | grep -q '"ok"' && echo 0 || echo 1)"

code=$(status "/api");        check "GET /api → 200"            "$([ "$code" = "200" ] && echo 0 || echo 1)"
body=$(get "/api");           check "returns nom=Nahman AI"     "$(echo "$body" | grep -q 'Nahman AI' && echo 0 || echo 1)"

code=$(status "/api/aide");   check "GET /api/aide → 200"       "$([ "$code" = "200" ] && echo 0 || echo 1)"
body=$(get "/api/aide");      check "has description key"       "$(echo "$body" | grep -q 'description' && echo 0 || echo 1)"

# ── 2. Static files ────────────────────────────────────────────────────────────
section "2. Static files (frontend)"

code=$(status "/");           check "GET / → 200"               "$([ "$code" = "200" ] && echo 0 || echo 1)"
body=$(get "/");              check "serves HTML"               "$(echo "$body" | grep -qi 'html' && echo 0 || echo 1)"

code=$(status "/chat.html");  check "GET /chat.html → 200"      "$([ "$code" = "200" ] && echo 0 || echo 1)"
body=$(get "/chat.html");     check "chat.html has Nahman AI"   "$(echo "$body" | grep -q 'Nahman AI' && echo 0 || echo 1)"

# ── 3. POST /api/chat ──────────────────────────────────────────────────────────
section "3. POST /api/chat"

code=$(post_status "/api/chat" '{"texte":"Dis juste OK."}')
check "POST /api/chat → 200" "$([ "$code" = "200" ] && echo 0 || echo 1)"

body=$(post "/api/chat" '{"texte":"Dis juste OK."}')
check "response has message key" "$(echo "$body" | grep -q '"message"' && echo 0 || echo 1)"
check "message is non-empty"     "$(echo "$body" | grep -q '"message":""' && echo 1 || echo 0)"

body=$(post "/api/chat" '{"texte":""}')
check "empty texte handled"      "$(echo "$body" | grep -q '"message"' && echo 0 || echo 1)"

body=$(post "/api/chat" '{"texte":"Reply PONG","system_prompt":"Always reply PONG."}')
check "system_prompt accepted"   "$(echo "$body" | grep -q '"message"' && echo 0 || echo 1)"

# ── 4. Config endpoints ────────────────────────────────────────────────────────
section "4. Config endpoints"

code=$(status "/api/config/prompt")
check "GET /api/config/prompt → 200"  "$([ "$code" = "200" ] && echo 0 || echo 1)"

body=$(get "/api/config/prompt")
check "has prompt_actuel key"         "$(echo "$body" | grep -q 'prompt_actuel' && echo 0 || echo 1)"

body=$(post "/api/config/prompt" '{"prompt":"Tu es un robot."}')
check "POST config/prompt updated"    "$(echo "$body" | grep -q 'mis' && echo 0 || echo 1)"

body=$(post "/api/config/prompt/reset" '{}')
check "POST config/prompt/reset ok"   "$(echo "$body" | grep -q 'prompt' && echo 0 || echo 1)"

# ── Summary ────────────────────────────────────────────────────────────────────
total=20
passed=$((total - failures))
echo -e "\n$(printf '─%.0s' {1..40})"
if [ "$failures" -eq 0 ]; then
  echo -e "\033[92m✓ All ${total} tests passed!\033[0m"
else
  echo -e "\033[91m✗ ${failures}/${total} tests failed.\033[0m"
  exit 1
fi
