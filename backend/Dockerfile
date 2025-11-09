

# Use an official Python runtime as a parent image, explicitly for ARM architecture
FROM python:3.11-slim-bullseye

# Set the working directory in the container
WORKDIR /app

# Copy requirements file and install dependencies first for caching
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    netcat-openbsd \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=5s \
  CMD curl -f http://localhost:8000/health || exit 1

# Copy simple entrypoint script and make it executable
COPY simple-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/simple-entrypoint.sh

# Set the entrypoint to our custom script
ENTRYPOINT ["/usr/local/bin/simple-entrypoint.sh"]

# Default command (will be overridden by entrypoint)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

