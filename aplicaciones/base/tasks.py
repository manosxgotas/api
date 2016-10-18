from __future__ import absolute_import

import datetime

from celery import shared_task

from django.conf import settings

from .models import (
    CodigoVerificacion,
    Donante,
    DIAS_DONACION_POR_GENERO
    )

from django.template import loader
from django.core.mail import EmailMultiAlternatives


def enviar_mail_recordatorio(donante):
    # URL de inicio
    home_url = settings.FRONTEND_URL + 'home'

    # Obtención de templates html y txt de emails.
    htmly = loader.get_template('emails/html/recordatorio_donacion.html')
    text = loader.get_template('emails/txt/recordatorio_donacion.txt')

    # Definición de variables de contexto
    variables = {
        'donante': donante,
        'home_url': home_url,
    }

    html_content = htmly.render(variables)
    text_content = text.render(variables)

    # Creación y envío de email.
    msg = EmailMultiAlternatives(
        '¡Ya puedes donar nuevamente en Manos por Gotas!',
        text_content,
        to=[donante.usuario.email]
    )

    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task(name='eliminar_codigos_vencidos')
def eliminar_codigos_vencidos():
    codigos = CodigoVerificacion.objects.all()
    for codigo in codigos:
        if codigo.fechaVencimiento >= datetime.date.today():
            codigo.delete()


@shared_task(name='enviar_recordatorio_donante')
def enviar_recordatorio_donante():
    donantes = Donante.objects.all()
    for donante in donantes:
        donaciones_donante = donante.registro.donaciones.order_by("fechaHora")

        # Si el donante posee donaciones
        if donaciones_donante:

            # Obtengo la fecha y hora de la última donación
            # realizada por el donante.
            ultima_donacion = donaciones_donante.last().fechaHora

            # Obtengo el género del donante.
            genero_donante = donante.genero

            # Calculo la diferencia de días entre la última donación
            # realizada por el donante y la fecha actual.
            dias_desde_ultima_donacion = datetime.datetime.now() - ultima_donacion

            # Dependiendo del sexo del donante obtengo la cantidad
            # de días necesarios para que el donante pueda realizar.
            # una nueva donación.
            dias_proxima_donacion = DIAS_DONACION_POR_GENERO[genero_donante] - dias_desde_ultima_donacion.days

            if dias_proxima_donacion == 0:
                enviar_mail_recordatorio(donante)
