#!/bin/bash
set -e

echo "Checking and creating database users..."

# Wait for database to be ready
while ! nc -z db 5432; do
  echo "Waiting for database..."
  sleep 1
done

echo "Database is ready, checking users..."

# First, try to connect as postgres user, if it doesn't exist, try other approaches
echo "Attempting to connect to database..."

# Try different connection approaches
DB_CONNECTED=false

# Approach 1: Try connecting as postgres user
if PGPASSWORD=postgres_password psql -h db -U postgres -d engineering_docs -c "SELECT 1;" >/dev/null 2>&1; then
    echo "Connected as postgres user"
    DB_CONNECTED=true
    SUPERUSER="postgres"
    SUPERUSER_PASSWORD="postgres_password"
elif PGPASSWORD=apppassword psql -h db -U appuser -d engineering_docs -c "SELECT 1;" >/dev/null 2>&1; then
    echo "Connected as appuser (already exists)"
    DB_CONNECTED=true
    echo "appuser already exists and is functional"
    exit 0
else
    echo "Trying to find existing superuser..."
    # Try to connect with common default users
    for user in postgres admin root; do
        for password in postgres_password postgres admin root ""; do
            if [ -n "$password" ]; then
                if PGPASSWORD="$password" psql -h db -U "$user" -d engineering_docs -c "SELECT 1;" >/dev/null 2>&1; then
                    echo "Connected as $user with password"
                    DB_CONNECTED=true
                    SUPERUSER="$user"
                    SUPERUSER_PASSWORD="$password"
                    break 2
                fi
            else
                if psql -h db -U "$user" -d engineering_docs -c "SELECT 1;" >/dev/null 2>&1; then
                    echo "Connected as $user without password"
                    DB_CONNECTED=true
                    SUPERUSER="$user"
                    SUPERUSER_PASSWORD=""
                    break 2
                fi
            fi
        done
    done
fi

if [ "$DB_CONNECTED" = false ]; then
    echo "Could not connect to database with any known credentials"
    echo "This might be a fresh database that needs manual setup"
    exit 1
fi

# Create the appuser role if it doesn't exist
echo "Creating appuser role using $SUPERUSER..."
if [ -n "$SUPERUSER_PASSWORD" ]; then
    PGPASSWORD="$SUPERUSER_PASSWORD" psql -h db -U "$SUPERUSER" -d engineering_docs -c "
    DO \$\$
    BEGIN
      IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'appuser') THEN
        CREATE ROLE appuser WITH LOGIN PASSWORD 'apppassword';
        ALTER ROLE appuser CREATEDB;
        GRANT ALL PRIVILEGES ON DATABASE engineering_docs TO appuser;
        RAISE NOTICE 'Created appuser role';
      ELSE
        RAISE NOTICE 'appuser role already exists';
      END IF;
    END \$\$;
    " || echo "Failed to create user, continuing anyway..."
else
    psql -h db -U "$SUPERUSER" -d engineering_docs -c "
    DO \$\$
    BEGIN
      IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'appuser') THEN
        CREATE ROLE appuser WITH LOGIN PASSWORD 'apppassword';
        ALTER ROLE appuser CREATEDB;
        GRANT ALL PRIVILEGES ON DATABASE engineering_docs TO appuser;
        RAISE NOTICE 'Created appuser role';
      ELSE
        RAISE NOTICE 'appuser role already exists';
      END IF;
    END \$\$;
    " || echo "Failed to create user, continuing anyway..."
fi

echo "User creation script completed!"