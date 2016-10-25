# coding=utf-8
import datetime
from django.contrib import admin

from ..models import (
    Evento,
    ImagenEvento,
    LugarEvento
    )


class ImagenEventoInline(admin.TabularInline):
    model = ImagenEvento


class LugarEventoInline(admin.TabularInline):
    model = LugarEvento


class EventoAdmin(admin.ModelAdmin):
    """
    Especificación de la representación de los eventos en la interfaz de administración.
    """
    empty_value_display = 'Valor no ingresado'
    list_display = (
        'nombre',
        '_estado',
        'fechaHoraInicio',
        'fechaHoraFin',
        '_categoria'
    )

    list_filter = (
        'categoria',
    )

    inlines = [
        ImagenEventoInline,
        LugarEventoInline
    ]

    def _estado(self, obj):
        fecha_actual = datetime.datetime.now()
        if fecha_actual < obj.fechaHoraInicio:
            return 'Próximamente'
        elif fecha_actual >= obj.fechaHoraInicio and fecha_actual < obj.fechaHoraFin:
            return '¡Ahora!'
        else:
            return 'Concluído'

    def _categoria(self, obj):
        return obj.categoria.nombre


admin.site.register(Evento, EventoAdmin)
