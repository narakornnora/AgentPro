#!/bin/bash
echo "=== AgentPro Installer ==="

if ! command -v docker &> /dev/null
then
    echo "Docker not found, please install Docker first."
    exit
fi

echo "[1/2] Building images..."
docker compose build

echo "[2/2] Starting containers..."
docker compose up -d

echo "=== Installation complete! Visit http://localhost:8080 ==="
