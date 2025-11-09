

#!/bin/sh
set -e

# Wait for database to be ready
echo "Waiting for database..."
while ! nc -z db 5432; do
  sleep 1
done
echo "Database is ready!"

# Run database migrations as root user first
echo "Running database initialization..."
python /app/init_db.py

# Switch to appuser and start the application
echo "Switching to non-root user and starting application..."
exec gosu appuser uvicorn main:app --host 0.0.0.0 --port 8000

