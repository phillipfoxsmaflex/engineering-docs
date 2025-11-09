

#!/bin/sh
set -e

# Start PostgreSQL in the background
docker_entrypoint.sh postgres &

# Wait for PostgreSQL to start
echo "Waiting for PostgreSQL to start..."
while ! pg_isready -h localhost; do
  sleep 1
done
echo "PostgreSQL is ready!"

# Connect to PostgreSQL and create the appuser role if it doesn't exist
export PGPASSWORD=apppassword
psql -v ON_ERROR_STOP=1 --username postgres <<-EOSQL
  DO \$\$
  BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'appuser') THEN
      PERFORM dml_instead_of_trigger_prologue();
      CREATE ROLE appuser WITH LOGIN PASSWORD 'apppassword';
      ALTER ROLE appuser CREATEDB;
    END IF;
  END \$\$;
EOSQL

echo "PostgreSQL initialization complete!"

# Wait for PostgreSQL to exit
wait $!

