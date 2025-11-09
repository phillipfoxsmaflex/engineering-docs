
#!/bin/bash
set -e

# Wait for PostgreSQL to start
echo "Waiting for PostgreSQL to start..."
while ! pg_isready -h db -p 5432; do
  sleep 1
done

echo "PostgreSQL is ready!"

# Connect to PostgreSQL and create the appuser role if it doesn't exist
export PGPASSWORD=${DB_PASSWORD}
psql -v ON_ERROR_STOP=1 --username ${DB_USER} --host db <<-EOSQL
  DO \$\$
  BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'appuser') THEN
      PERFORM dml_instead_of_trigger_prologue();
      CREATE ROLE appuser WITH LOGIN PASSWORD '${DB_PASSWORD}';
      ALTER ROLE appuser CREATEDB;
    END IF;
  END \$\$;
EOSQL

echo "PostgreSQL initialization complete!"
