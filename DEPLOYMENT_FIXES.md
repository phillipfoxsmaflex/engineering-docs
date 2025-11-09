# Docker Compose Deployment Fixes

This document outlines the fixes applied to resolve Docker Compose deployment issues.

## Issues Fixed

### 1. Python Import Error
**Problem**: `ImportError: attempted relative import with no known parent package`
**Solution**: Changed relative imports to absolute imports in `main.py`

### 2. Database User Creation
**Problem**: `FATAL: role "appuser" does not exist`
**Solution**: Created `create-user.sh` script that runs during backend startup to ensure the database user exists

### 3. Database Initialization Skipping
**Problem**: Database initialization scripts not running on existing volumes
**Solution**: Added runtime user creation script that runs every time the backend starts

## Files Modified

- `backend/main.py` - Fixed import statements
- `backend/simple-entrypoint.sh` - Added user creation step
- `backend/create-user.sh` - New script to create database user
- `backend/Dockerfile` - Added postgresql-client package
- `.env` - Environment variables for Docker Compose

## Deployment Instructions

1. **Clean up existing Docker state** (if you have previous failed deployments):
   ```bash
   ./cleanup-docker.sh
   ```

2. **Build and start the application**:
   ```bash
   docker-compose up --build
   ```

3. **Access the application**:
   - Main Application: http://localhost:8081
   - Backend API: http://localhost:8000
   - Frontend: http://localhost:3001

## Troubleshooting

If you still encounter issues:

1. **Check logs**:
   ```bash
   docker-compose logs backend
   docker-compose logs db
   ```

2. **Restart with fresh volumes**:
   ```bash
   docker-compose down -v
   docker-compose up --build
   ```

3. **Verify database connection**:
   ```bash
   docker-compose exec db psql -U appuser -d engineering_docs -c "\dt"
   ```