

#!/bin/bash
set -e

echo "Creating appuser role..."

# Create the appuser role if it doesn't exist
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
  DO \$\$
  BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'appuser') THEN
      CREATE ROLE appuser WITH LOGIN PASSWORD 'apppassword';
      ALTER ROLE appuser CREATEDB;
      GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB TO appuser;
      RAISE NOTICE 'Created appuser role successfully';
    ELSE
      RAISE NOTICE 'appuser role already exists';
    END IF;
  END \$\$;
EOSQL

echo "PostgreSQL initialization complete!"

