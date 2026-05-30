#!/usr/bin/env bash
set -euo pipefail

COMPOSE="docker compose -f docker-compose.yml -f compose/integration/job-service.yml"

cleanup() {
  echo "Stopping job-service integration test stack..."
  $COMPOSE down -v
}

trap cleanup EXIT

echo "Starting RabbitMQ and job-service..."
$COMPOSE up -d --build rabbitmq job-service

echo "Running job-service integration tests..."
pytest -m integration job-service/tests/integration