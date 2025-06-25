#!/bin/bash
echo "Applying migrations..."
alembic upgrade head

echo "Starting FastAPI server..."
exec uvicorn src.main:app --host 0.0.0.0 --port 8000