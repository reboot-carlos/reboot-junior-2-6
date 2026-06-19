#!/usr/bin/env bash
# Stream live logs from the running container
cd "$(dirname "$0")/.."
docker compose logs -f
