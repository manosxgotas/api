# coding=utf-8

from django.contrib import admin

from ..models import Provincia


class ProvinciaAdmin(admin.ModelAdmin):
    """
    Especificación de la representación de Provincia en la interfaz de administración.
    """
    empty_value_display = 'Valor no ingresado'
    list_display = (
        'nombre',
    )


admin.site.register(Provincia, ProvinciaAdmin)