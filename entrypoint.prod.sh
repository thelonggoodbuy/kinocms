#!/bin/sh


if [ "$DATABASE" = "postgres" ]
then
    echo "waiting for postgres..."

    while ! nc-z $SQL_HOST $SQL_PORT; do
        sleep 0.1
    done

    echo "PostgreSQL started"

fi

# python -m pip install Pillow
# python manage.py flush --no-input
python manage.py migrate
python manage.py main_initial_script
python manage.py shows_initial_script
python manage.py generate_initial_superuser
python manage.py generate_initial_simple_users
python manage.py generate_initial_buying_tickets
python manage.py collectstatic


exec "$@"