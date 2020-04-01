web: gunicorn newsfeed.wsgi
worker: celery -A newsfeed worker -B -l info
