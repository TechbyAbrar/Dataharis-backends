#!/bin/sh

echo "Waiting for PostgreSQL..."

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 1
done

echo "PostgreSQL started."

# Apply migrations & collect static
python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec "$@"
