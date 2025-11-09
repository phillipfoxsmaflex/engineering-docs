#!/bin/bash
set -e

echo "Checking and creating appuser role..."

# Wait for database to be ready
while ! nc -z db 5432; do
  echo "Waiting for database..."
  sleep 1
done

echo "Database is ready, creating appuser..."

# Create the appuser role if it doesn't exist
PGPASSWORD=$DB_PASSWORD psql -h db -U $DB_USER -d $DB_NAME -c "
DO \$\$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'appuser') THEN
    CREATE ROLE appuser WITH LOGIN PASSWORD 'apppassword';
    ALTER ROLE appuser CREATEDB;
    GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO appuser;
    RAISE NOTICE 'Created appuser role';
  ELSE
    RAISE NOTICE 'appuser role already exists';
  END IF;
END \$\$;
" || echo "Failed to create user, continuing anyway..."

echo "User creation script completed!"