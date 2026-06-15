#!/usr/bin/env bash
set -euo pipefail
# wger DRF token auth: POST /api/v2/login/ {username,password} -> {"token": "..."}
# The token is sent as: Authorization: Token <token>
U="${WGER_ADMIN:-admin}"; P="${WGER_PASS:-adminadmin}"

# Wait for service to be ready
for i in $(seq 1 60); do
  if curl -sf -m5 -o /dev/null http://localhost:8091/api/v2/version/; then break; fi
  sleep 3
  [ "$i" = 60 ] && { echo "Service not ready after 180s" >&2; exit 1; }
done

curl -sf -X POST "http://localhost:8091/api/v2/login/" \
  -H 'Content-Type: application/json' \
  -d "{\"username\":\"$U\",\"password\":\"$P\"}" \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])"
