

# Engineering Document Management System Deployment Guide

This guide will walk you through deploying the Engineering Document Management System using Docker Compose.

## Prerequisites

- Docker installed on your system
- Docker Compose installed on your system

## Getting Started

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/engineering-docs.git
   cd engineering-docs
   ```

2. **Build and start the services:**

   ```bash
   docker-compose up --build
   ```

3. **Access the application:**

   Open your web browser and navigate to `http://localhost:3000` for the frontend and `http://localhost:8000` for the backend API.

## Directory Structure

- `backend/`: Contains the FastAPI backend code.
- `frontend/`: Contains the React frontend code.
- `docker-compose.yml`: Docker Compose configuration file.

## Configuration

### Environment Variables

The application uses environment variables for configuration. You can set these in a `.env` file at the root of the project:

```
# Backend
BACKEND_DATABASE_URL=sqlite:///./test.db
BACKEND_SECRET_KEY=your_secret_key

# Frontend
REACT_APP_API_BASE_URL=http://localhost:8000
```

## Running Tests

To run tests, use the following commands:

```bash
# Run backend tests
docker-compose run backend pytest

# Run frontend tests
docker-compose run frontend npm test
```

## Stopping the Services

To stop the services, press `Ctrl+C` in the terminal where Docker Compose is running or use:

```bash
docker-compose down
```

## Troubleshooting

- If you encounter issues with database migrations, try running:
  ```bash
  docker-compose run backend alembic upgrade head
  ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

