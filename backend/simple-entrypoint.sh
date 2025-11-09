#!/bin/bash
set -e

# Wait for database to be ready
echo "Waiting for database..."
while ! nc -z db 5432; do
  sleep 1
done
echo "Database is ready!"

# Create database user if needed
echo "Creating database user..."
/app/create-user.sh

# Run the application directly (without user switching to avoid permission issues)
echo "Starting application..."
exec uvicorn main:app --host 0.0.0.0 --port 8000