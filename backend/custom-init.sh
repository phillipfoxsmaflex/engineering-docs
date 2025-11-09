

#!/bin/bash
set -e

echo "🚀 Starting PostgreSQL initialization..."
echo "Database: $POSTGRES_DB"
echo "User: $POSTGRES_USER"

# Ensure the main database exists
echo "📋 Ensuring database exists..."
# Check if database exists and create it if it doesn't
DB_EXISTS=$(psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "postgres" -tAc "SELECT 1 FROM pg_database WHERE datname='$POSTGRES_DB'")
if [ "$DB_EXISTS" != "1" ]; then
  echo "Creating database $POSTGRES_DB..."
  psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "postgres" -c "CREATE DATABASE $POSTGRES_DB;"
  echo "✅ Database $POSTGRES_DB created successfully"
else
  echo "✅ Database $POSTGRES_DB already exists"
fi

# Create the appuser role
echo "👤 Creating appuser role..."
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
  DO \$\$
  BEGIN
    -- Check if appuser exists
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'appuser') THEN
      CREATE ROLE appuser WITH LOGIN PASSWORD 'apppassword';
      ALTER ROLE appuser CREATEDB;
      GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB TO appuser;
      RAISE NOTICE '✅ Created appuser role successfully';
    ELSE
      RAISE NOTICE '✅ appuser role already exists';
    END IF;
    
    -- Ensure appuser has correct permissions
    GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB TO appuser;
    ALTER ROLE appuser CREATEDB;
    
    RAISE NOTICE '✅ appuser permissions updated';
  END \$\$;
EOSQL

# Test the connections
echo "🧪 Testing database connections..."
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" -c "SELECT 'postgres user connection: OK' as test_result;"
psql -v ON_ERROR_STOP=1 --username "appuser" --dbname "$POSTGRES_DB" -c "SELECT 'appuser connection: OK' as test_result;" || echo "⚠️  appuser connection test failed, but user should be created"

echo "✅ PostgreSQL initialization complete!"
echo "📋 Available users:"
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" -c "SELECT rolname, rolsuper, rolcreatedb, rolcanlogin FROM pg_roles WHERE rolname IN ('postgres', 'appuser');"

