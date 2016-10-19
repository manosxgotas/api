# coding=utf-8
import datetime

from django.contrib import admin
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf.urls import url

from .historicoEstadoDonacion import HistoricoEstadoDonacionInline

from ..models import (
    Donacion,
    EstadoDonacion,
    HistoricoEstadoDonacion
)

ESTADO_PENDIENTE = 'pendiente'
ESTADO_VERIFICADA = 'verificada'


def get_estado_donacion(donacion):
    estado_donacion = None
    historicos = donacion.historicoEstados
    if historicos.exists():
        ultimo_historico = historicos.last()
        estado_donacion = ultimo_historico.estado.nombre
    return estado_donacion


class DonacionAdmin(admin.ModelAdmin):
    """
    Especificación de la representación del estado de la solicitud de
     donación en la interfaz de administración.
    """
    # Método para agregar nueva url para generar códigos de verificación en el
    # sitio de administración.
    def get_urls(self):
        urls = super(DonacionAdmin, self).get_urls()
        add_urls = [
            url(
                r'^verificar/(?P<donacion_id>\d+)$',
                self.admin_site.admin_view(self.verificar),
                name='base_donacion_verificar',
            ),
            url(
                r'^rechazar/(?P<donacion_id>\d+)$',
                self.admin_site.admin_view(self.rechazar),
                name='base_donacion_rechazar',
            )
        ]
        return add_urls + urls

    def verificar(self, request, donacion_id):
        donacion_qs = Donacion.objects.filter(id=donacion_id)
        if donacion_qs.exists():
            donacion_obj = donacion_qs.first()
            historicos = donacion_obj.historicoEstados
            if historicos.exists():
                ultimo_historico = historicos.last()
                ultimo_historico.fin = datetime.datetime.now()
                ultimo_historico.save()
                estado_verificada = EstadoDonacion.objects.get(nombre="Verificada")
                HistoricoEstadoDonacion.objects.create(
                    inicio=datetime.datetime.now(),
                    donacion=donacion_obj,
                    estado=estado_verificada,
                )
        return HttpResponseRedirect(
            reverse(
                'admin:base_donacion_changelist'
            )
        )

    def rechazar(self, request, donacion_id):
        donacion_qs = Donacion.objects.filter(id=donacion_id)
        if donacion_qs.exists():
            donacion_obj = donacion_qs.first()
            historicos = donacion_obj.historicoEstados
            if historicos.exists():
                ultimo_historico = historicos.last()
                ultimo_historico.fin = datetime.datetime.now()
                ultimo_historico.save()
                estado_sin_verificar = EstadoDonacion.objects.get(nombre="Sin verificar")
                HistoricoEstadoDonacion.objects.create(
                    inicio=datetime.datetime.now(),
                    donacion=donacion_obj,
                    estado=estado_sin_verificar,
                )
        return HttpResponseRedirect(
            reverse(
                'admin:base_donacion_changelist'
            )
        )

    empty_value_display = '--------'
    list_display = (
        'id',
        '_usuario',
        'estado_donacion',
        'foto',
        'fechaHora',
        'imagen_verificacion',
        'boton_verificacion'
    )

    inlines = [
        HistoricoEstadoDonacionInline,
    ]

    def estado_donacion(self, obj):
        return get_estado_donacion(obj)

    def boton_verificacion(self, obj):
        estado_donacion = get_estado_donacion(obj)
        if estado_donacion is not None and estado_donacion.lower() == ESTADO_PENDIENTE:
            link_verificacion = reverse('admin:base_donacion_verificar', args=[obj.id])
            link_rechazo = reverse('admin:base_donacion_rechazar', args=[obj.id])
            return "<a class='addlink' href='{0!s}' >Verificar</a> <a class='deletelink' href='{1!s}'>Rechazar</a>".format(
                link_verificacion,
                link_rechazo
            )
        else:
            return "--------"
    boton_verificacion.short_description = 'Verificar donación'
    boton_verificacion.allow_tags = True

    def _usuario(self, obj):
        return obj.registro.donante

    def _estadoDonacion(self, obj):
        return obj.historicoEstados.estado.nombre

admin.site.register(Donacion, DonacionAdmin)
