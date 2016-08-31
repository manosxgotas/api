# coding=utf-8

from django.contrib import admin

from ..models import RegistroDonacion


class RegistroDonacionAdmin(admin.ModelAdmin):
    """
    Especificación de la representación del registro de
     donación en la interfaz de administración.
    """
    empty_value_display = 'Valor no ingresado'
    list_display = (
        'id',
        '_donante',
    )


    def _donante(self, obj):
        return obj.donante.usuario

admin.site.register(RegistroDonacion, RegistroDonacionAdmin)