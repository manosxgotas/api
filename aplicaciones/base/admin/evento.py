# coding=utf-8

from django.contrib import admin

from ..models import Evento


class EventoAdmin(admin.ModelAdmin):
    """
    Especificación de la representación de los eventos en la interfaz de administración.
    """
    empty_value_display = 'Valor no ingresado'
    list_display = (
        'nombre',
        'fechaHoraInicio',
        'fechaHoraFin',
        '_categoria'
    )

    list_filter = (
        'categoria',
    )

    def _categoria(self,obj):
        return obj.categoria.nombre


admin.site.register(Evento, EventoAdmin)