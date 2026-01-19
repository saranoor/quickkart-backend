from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
app = Celery('backend')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self, id):
    print('Request: {0!r}'.format(self.request))
    print(f"I will keep running for 20 seconds...")
    print(f"Id received: {id}")
    for i in range(6):
            time.sleep(1)
            if i % 5 == 0:
                print(f"Task is still running... second {i}")
    print(f"send an email to user {id}")
    return "Finished fully"
