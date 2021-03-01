web: gunicorn WeatherReminder.wsgi --log-file -
worker: celery -A WeatherReminder worker --beat --scheduler django --loglevel=info