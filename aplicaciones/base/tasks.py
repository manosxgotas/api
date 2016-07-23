from __future__ import absolute_import

import datetime

from celery import shared_task

from .models import CodigoVerificacion


@shared_task(name='eliminar_codigos_vencidos')
def eliminar_codigos_vencidos():
    codigos = CodigoVerificacion.objects.all()
    for codigo in codigos:
        if codigo.fechaVencimiento >= datetime.date.today():
            codigo.delete()