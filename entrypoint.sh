#!/bin/sh

echo "Waiting for PostgreSQL to be ready..."
until pg_isready -h "$DB_HOST" -p 5432; do
  echo "Postgres is unavailable - sleeping"
  sleep 1
done

echo "PostgreSQL is ready."

echo "Running migrations..."
alembic upgrade head

echo "Starting FastAPI server..."
exec uvicorn src.main:app --host 0.0.0.0 --port 8000
