
-- Create appuser role if it doesn't exist
DO $$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'appuser') THEN
    PERFORM dml_instead_of_trigger_prologue();
    CREATE ROLE appuser WITH LOGIN PASSWORD 'apppassword';
    ALTER ROLE appuser CREATEDB;
  END IF;
END $$;

-- Grant all privileges on the engineering_docs database to appuser
GRANT ALL PRIVILEGES ON DATABASE engineering_docs TO appuser;
