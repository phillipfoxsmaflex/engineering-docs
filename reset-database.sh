#!/bin/bash

echo "🔄 Resetting database and volumes for clean deployment..."

# Stop all containers
echo "📦 Stopping all containers..."
docker compose down -v --remove-orphans

# List and remove all project volumes
echo "🗑️  Removing all project volumes..."
PROJECT_NAME="engineering-docs"

# Get all volumes for this project
VOLUMES=$(docker volume ls -q | grep "^${PROJECT_NAME}_" 2>/dev/null || true)

if [ -n "$VOLUMES" ]; then
    echo "Found volumes to remove: $VOLUMES"
    echo "$VOLUMES" | xargs docker volume rm 2>/dev/null || echo "Some volumes were already removed"
else
    echo "No project volumes found to remove"
fi

# Also try common volume names
docker volume rm engineering-docs_postgres_data 2>/dev/null || echo "postgres_data volume not found"
docker volume rm engineering-docs_uploads 2>/dev/null || echo "uploads volume not found"
docker volume rm engineering-docs_certs 2>/dev/null || echo "certs volume not found"

# Remove any orphaned containers
echo "🧹 Cleaning up orphaned containers..."
docker compose rm -f 2>/dev/null || true

# Remove any dangling images for this project
echo "🖼️  Removing project images..."
docker images | grep "engineering-docs" | awk '{print $3}' | xargs docker rmi -f 2>/dev/null || echo "No project images to remove"

# Clean up Docker system (optional)
echo "🧽 Cleaning up Docker system..."
docker system prune -f

echo ""
echo "✅ Database reset complete!"
echo ""
echo "🚀 You can now run a clean deployment with:"
echo "   docker compose up --build"
echo ""
echo "📋 This will:"
echo "   - Create fresh PostgreSQL database with postgres superuser"
echo "   - Run initialization scripts to create appuser"
echo "   - Start all services with clean state"