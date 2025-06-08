#!/bin/sh

export FLASK_APP=app

echo "Waiting for database..."
timeout=60
count=0
while ! nc -z db 3306; do
  sleep 1
  count=$((count+1))
  if [ $count -ge $timeout ]; then
    echo "Banco de dados não respondeu após $timeout segundos, abortando."
    exit 1
  fi
done
echo "Database connection is ready."

if [ ! -d "migrations" ]; then
    echo "Initializing database migrations folder..."
    flask db init
fi

echo "Applying database migrations..."
flask db upgrade

echo "Starting Flask development server..."
exec flask run --host=0.0.0.0
