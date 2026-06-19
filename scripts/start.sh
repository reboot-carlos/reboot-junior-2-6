#!/usr/bin/env bash
# Build and start the app with Docker
set -euo pipefail

cd "$(dirname "$0")/.."

if [ ! -f .env ]; then
  echo "ERROR: .env file not found. Copy .env.example and fill in your API key:"
  echo "  cp .env.example .env"
  exit 1
fi

echo "Building and starting Nahman AI..."
docker compose up --build -d

echo ""
echo "Waiting for server to be ready..."
for i in $(seq 1 20); do
  if curl -sf http://localhost:8000/api/health > /dev/null 2>&1; then
    echo ""
    echo "Nahman AI is running!"
    echo "  Frontend : http://localhost:8000"
    echo "  API docs : http://localhost:8000/docs"
    echo ""
    echo "To stop: bash scripts/stop.sh"
    exit 0
  fi
  sleep 1
done

echo "ERROR: Server did not start in time. Check logs:"
echo "  docker compose logs"
exit 1
