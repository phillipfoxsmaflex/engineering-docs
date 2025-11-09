#!/bin/bash

echo "Cleaning up Docker containers and volumes..."

# Stop and remove all containers
docker-compose down

# Remove all volumes to force fresh database
docker-compose down -v

# Remove any orphaned containers
docker container prune -f

# Remove any unused volumes
docker volume prune -f

echo "Docker cleanup complete!"
echo "You can now run: docker-compose up --build"