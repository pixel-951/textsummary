#!/usr/bin/env bash
set -euo pipefail

export FRONTEND_PORT="${FRONTEND_PORT:-8080}"
export BASE_URL="${BASE_URL:-http://localhost:${FRONTEND_PORT}}"

cleanup() {
  echo "Stopping Compose stack..."
  FRONTEND_PORT="$FRONTEND_PORT" docker compose down -v
}

trap cleanup EXIT

echo "Starting Compose stack on ${BASE_URL}..."
FRONTEND_PORT="$FRONTEND_PORT" docker compose up -d --build frontend

echo "Waiting for stack..."
for i in {1..60}; do
  if python -c "import urllib.request; urllib.request.urlopen('${BASE_URL}/', timeout=5)" >/dev/null 2>&1; then
    echo "Stack is reachable at ${BASE_URL}"
    break
  fi

  if [ "$i" -eq 60 ]; then
    echo "Stack did not become reachable"
    docker compose ps
    docker compose logs --no-color
    exit 1
  fi

  sleep 2
done

echo "Running system tests..."
pytest -m system tests/system