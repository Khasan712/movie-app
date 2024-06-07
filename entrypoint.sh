#!/bin/sh
echo 'entrypoint in >>>>>>>>'
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput
gunicorn config.wsgi:application --workers 4 --worker-class gevent --bind 0.0.0.0:8060 --backlog 1000 --timeout 30 --graceful-timeout 30 --max-requests 1000 --max-requests-jitter 100
#python manage.py runserver 0.0.0.0:8080
echo '>>>>>>>> Exiting entrypoint'
