#!/bin/bash

echo "🔧 Attempting to fix existing database without reset..."

# Stop backend container to avoid conflicts
echo "📦 Stopping backend container..."
docker compose stop backend

# Start only the database container
echo "🗄️  Starting database container..."
docker compose up -d db

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
sleep 10

# Try to connect as any existing superuser or create one
echo "🔑 Attempting to create postgres superuser..."

# Method 1: Try to connect to the database directly and create users
docker compose exec db psql -U postgres -d postgres -c "SELECT version();" 2>/dev/null && echo "✅ postgres user exists" || {
    echo "❌ postgres user does not exist, trying alternative approach..."
    
    # Method 2: Try to access as any user that might exist
    # This is a more complex approach - we'll try to create a superuser from within the container
    docker compose exec db sh -c '
        echo "Attempting to create postgres superuser from within container..."
        
        # Try to initialize the database manually
        if [ ! -f /var/lib/postgresql/data/PG_VERSION ]; then
            echo "Database not initialized, initializing now..."
            su-exec postgres initdb -D /var/lib/postgresql/data
        fi
        
        # Start postgres in single-user mode to create superuser
        echo "Creating postgres superuser in single-user mode..."
        su-exec postgres postgres --single -D /var/lib/postgresql/data postgres <<EOF
CREATE USER postgres WITH SUPERUSER PASSWORD '\''postgres_password'\'';
CREATE DATABASE engineering_docs OWNER postgres;
\q
EOF
        
        echo "Superuser creation attempt completed"
    ' || echo "Failed to create superuser from within container"
}

# Now try to create the appuser
echo "👤 Creating appuser..."
docker compose exec db psql -U postgres -d engineering_docs -c "
DO \$\$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'appuser') THEN
    CREATE ROLE appuser WITH LOGIN PASSWORD 'apppassword';
    ALTER ROLE appuser CREATEDB;
    GRANT ALL PRIVILEGES ON DATABASE engineering_docs TO appuser;
    RAISE NOTICE 'Created appuser role successfully';
  ELSE
    RAISE NOTICE 'appuser role already exists';
  END IF;
END \$\$;
" 2>/dev/null && echo "✅ appuser created successfully" || echo "❌ Failed to create appuser"

# Test the connection
echo "🧪 Testing database connections..."
docker compose exec db psql -U postgres -d engineering_docs -c "SELECT 'postgres user works' as test;" 2>/dev/null && echo "✅ postgres connection works"
docker compose exec db psql -U appuser -d engineering_docs -c "SELECT 'appuser works' as test;" 2>/dev/null && echo "✅ appuser connection works"

echo ""
echo "🚀 Database fix attempt completed. Starting all services..."
docker compose up -d

echo ""
echo "📋 Check the logs with: docker compose logs -f backend"