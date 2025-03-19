#!/bin/sh

echo "Waiting for PostgreSQL to start..."
while ! pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; do
  sleep 1
done

echo "PostgreSQL is up, running migrations..."
flask db upgrade || { echo "Migration failed"; exit 1; }

echo "Starting Flask app..."
exec flask run --host=0.0.0.0 --port=5000