



#!/bin/bash
set -e

# Wait for database
echo "Waiting for database..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done
echo "Database is ready!"

# Run database migrations
echo "Running database migrations..."
python init_db.py

# Create uploads directory if it doesn't exist
mkdir -p /app/uploads

# Start the application with gunicorn in production mode
echo "Starting application with gunicorn..."
exec gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000


