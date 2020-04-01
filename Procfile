web: gunicorn newsfeed.wsgi
worker: celery -A newsfeed worker -l info
beat: celery -A newsfeed beat -l info
