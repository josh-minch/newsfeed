'''
Celery configuration file for creating tasks
We set the pidfile with no path because celery does not clean up the celerybeat.pid
after it is killed
From root folder, run beat with
    celery -A newsfeed beat -l info --pidfile=
and worker with
    celery -A newsfeed worker -l info
'''
from __future__ import absolute_import, unicode_literals
import os
import platform

from celery import Celery


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newsfeed.settings')
# We must set the following env var to support running tasks on Windows
# See https://github.com/celery/celery/issues/4081
if platform.system() == 'Windows':
    os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

app = Celery('newsfeed')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
