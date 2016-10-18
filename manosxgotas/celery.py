from __future__ import absolute_import

import os

from datetime import timedelta

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'manosxgotas.settings.local')

from django.conf import settings  # noqa

app = Celery('manosxgotas')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.CELERYBEAT_SCHEDULE = {
    'eliminar_codigos_vencidos': {
        'task': 'eliminar_codigos_vencidos',
        'schedule': timedelta(days=1)
    },
    'enviar_recordatorio_donante': {
        'task': 'enviar_recordatorio_donante',
        'schedule': timedelta(hours=12)
    },
}


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
