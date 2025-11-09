

# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements file and install dependencies first for caching
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root user to run the application
RUN useradd -m appuser && chown -R appuser:appuser /app

# Copy the rest of the application code to the container
COPY . .

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=5s \
  CMD curl -f http://localhost:8000/health || exit 1

# Copy entrypoint script and make it executable
COPY docker-entrypoint.sh /usr/local/bin/
RUN dos2unix /usr/local/bin/docker-entrypoint.sh && \
    chmod +x /usr/local/bin/docker-entrypoint.sh

# Set the entrypoint to our custom script
ENTRYPOINT ["docker-entrypoint.sh"]

# Run uvicorn server when the container launches as non-root user
USER appuser
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

