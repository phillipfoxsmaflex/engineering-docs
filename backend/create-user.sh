#!/bin/bash
set -e

echo "Checking and creating database users..."

# Use environment variables with defaults
DB_HOST="${DB_HOST:-db}"
DB_PORT="${DB_PORT:-5432}"
DB_NAME="${DB_NAME:-engineering_docs}"
DB_USER="${DB_USER:-postgres}"
DB_PASSWORD="${DB_PASSWORD:-apppassword}"
APP_DB_USER="${APP_DB_USER:-appuser}"
APP_DB_PASSWORD="${APP_DB_PASSWORD:-apppassword}"

# Wait for database to be ready
while ! nc -z "$DB_HOST" "$DB_PORT"; do
  echo "Waiting for database..."
  sleep 1
done

echo "Database is ready, checking users..."

# Try to connect as the main database user
echo "Attempting to connect to database as $DB_USER..."

if PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -c "SELECT 1;" >/dev/null 2>&1; then
    echo "✅ Connected as $DB_USER user"
    
    # Check if app user already exists
    if PGPASSWORD="$APP_DB_PASSWORD" psql -h "$DB_HOST" -U "$APP_DB_USER" -d "$DB_NAME" -c "SELECT 1;" >/dev/null 2>&1; then
        echo "✅ $APP_DB_USER already exists and is functional"
        exit 0
    fi
    
    # Create the app user role if it doesn't exist
    echo "Creating $APP_DB_USER role..."
    PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -c "
    DO \$\$
    BEGIN
      IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = '$APP_DB_USER') THEN
        CREATE ROLE $APP_DB_USER WITH LOGIN PASSWORD '$APP_DB_PASSWORD';
        ALTER ROLE $APP_DB_USER CREATEDB;
        GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $APP_DB_USER;
        RAISE NOTICE '✅ Created $APP_DB_USER role';
      ELSE
        RAISE NOTICE '✅ $APP_DB_USER role already exists';
      END IF;
    END \$\$;
    " || echo "⚠️ Failed to create user, continuing anyway..."
    
    echo "✅ User creation script completed!"
else
    echo "❌ Could not connect to database as $DB_USER"
    echo "This might indicate a configuration issue"
    exit 1
fi