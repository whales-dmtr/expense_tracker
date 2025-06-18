#!/bin/sh
set -e

echo "Waiting for DB to be ready..."
until pg_isready -h db -U "$DB_USER" -d "$DB_NAME"; do
  echo "Postgres is unavailable - sleeping"
  sleep 2
done

echo "Running migrations..."
alembic upgrade head

echo "Starting app..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
