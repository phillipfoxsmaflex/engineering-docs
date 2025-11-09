



#!/bin/bash
set -e

# Make sure we're using bash
if [ "$(id -u)" = "0" ]; then
  echo "Switching to non-root user..."
  exec gosu appuser "$0" "$@"
fi

# Wait for database
echo "Waiting for database..."
while ! nc -z db 5432; do
  sleep 1
done
echo "Database is ready!"

# Run database migrations
echo "Running database migrations..."
python init_db.py

# Create uploads directory if it doesn't exist
mkdir -p /app/uploads

# Start the application with uvicorn directly (more compatible)
echo "Starting application with uvicorn..."
exec uvicorn main:app --host 0.0.0.0 --port 8000


