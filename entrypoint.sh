#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python /app/src/manage.py collectstatic --noinput
python /app/src/manage.py migrate
python /app/src/manage.py loaddata /app/src/fixtures/Group.json

exec "$@"