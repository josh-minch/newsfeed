web: gunicorn newsfeed.wsgi
worker: celery -A newsfeed worker -B -E -l info
