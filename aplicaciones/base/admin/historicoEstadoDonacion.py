# coding=utf-8

from django.contrib import admin

from ..models import HistoricoEstadoDonacion


class HistoricoEstadoDonacionAdmin(admin.ModelAdmin):
    """
    Especificación de la representación del historico del estado de la
     donación en la interfaz de administración.
    """
    empty_value_display = 'Valor no ingresado'
    list_display = (
        'id',
        '_usuario',
        'estado',
        'inicio',
        'fin',
    )
    list_filter = (
        'estado',
    )


    def _usuario(self, obj):
        return obj.donacion.registro.donante.usuario

admin.site.register(HistoricoEstadoDonacion, HistoricoEstadoDonacionAdmin)