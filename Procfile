release: python manage.py migrate --noinput && python manage.py collectstatic --noinput
web: gunicorn parking_App.wsgi --bind 0.0.0.0:$PORT
