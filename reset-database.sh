#!/bin/bash

echo "Resetting database and volumes..."

# Stop all containers
echo "Stopping containers..."
docker compose down

# Remove volumes to force fresh database initialization
echo "Removing volumes..."
docker volume rm engineering-docs_postgres_data 2>/dev/null || echo "postgres_data volume not found"
docker volume rm engineering-docs_uploads 2>/dev/null || echo "uploads volume not found"
docker volume rm engineering-docs_certs 2>/dev/null || echo "certs volume not found"

# Remove any orphaned containers
echo "Removing orphaned containers..."
docker compose rm -f

echo "Database reset complete. You can now run 'docker compose up --build'"