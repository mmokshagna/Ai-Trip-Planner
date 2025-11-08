#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Building backend image..."
docker build -t backend "$PROJECT_ROOT/backend"

echo "Building frontend image..."
docker build -t frontend "$PROJECT_ROOT/frontend"

echo "running docker compose..."
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:5173 (dev) or http://localhost:4173 (preview)"
docker compose up

