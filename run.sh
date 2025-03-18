#!/bin/bash
set -e

# Wait for PostgreSQL to become available
until pg_isready -h $POSTGRES_HOST -p 5432 -U $POSTGRES_USER; do
  echo "Waiting for PostgreSQL to become available..."
  sleep 1
done

echo "PostgreSQL is up and ready."

# Run your application
alembic upgrade head
python main.py

# This script will be executed when the container starts
# You can add any additional commands you need here
