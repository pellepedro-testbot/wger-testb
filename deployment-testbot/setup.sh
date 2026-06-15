#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
echo "Building wger from source + starting (slow first run — Python wheels, JS/CSS build, migrations, fixtures)..."
docker compose -f docker-compose.yml up -d --build
echo "Waiting for health on :8091 (up to ~10 min for first-run build + migrate + fixture load)..."
for i in $(seq 1 200); do
  if curl -sf -m5 -o /dev/null http://localhost:8091/api/v2/version/; then
    echo "healthy after $((i*3))s"
    break
  fi
  sleep 3
  [ "$i" = 200 ] && { echo "unhealthy after 600s — dumping logs"; docker compose -f docker-compose.yml logs --tail 200; exit 1; }
done
echo "Setup complete"
