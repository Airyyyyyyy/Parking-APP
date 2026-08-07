web: python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn parking_App.wsgi --bind 0.0.0.0:$PORT
