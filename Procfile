release: ./manage.py migrate
web: gunicorn --bind 0.0.0.0:$PORT danesfield.wsgi
worker: REMAP_SIGTERM=SIGQUIT celery --app danesfield.celery worker --loglevel INFO --without-heartbeat
