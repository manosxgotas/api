# coding=utf-8

from django.contrib import admin

from ..models import Donacion


class DonacionAdmin(admin.ModelAdmin):
    """
    Especificación de la representación del estado de la solicitud de
     donación en la interfaz de administración.
    """
    empty_value_display = 'Valor no ingresado'
    list_display = (
        'id',
        '_usuario',
        'foto',
        'fechaHora',
    )


    def _usuario(self, obj):
        return obj.registro.donante

    def _estadoDonacion(self, obj):
        return obj.historicoEstados.estado.nombre


admin.site.register(Donacion, DonacionAdmin)