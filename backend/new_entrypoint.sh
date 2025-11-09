
#!/bin/sh
set -e

# Run the official entrypoint script with all its arguments
exec docker-entrypoint.sh "$@"
