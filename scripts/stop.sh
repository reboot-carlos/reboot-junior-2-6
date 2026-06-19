#!/usr/bin/env bash
# Stop and remove the Docker containers
set -euo pipefail

cd "$(dirname "$0")/.."

echo "Stopping Nahman AI..."
docker compose down
echo "Done."
