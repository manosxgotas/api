# coding=utf-8

from django.contrib import admin

from ..models import Localidad


class LocalidadAdmin(admin.ModelAdmin):
    """
    Especificación de la representación de Localidad en la interfaz de administración.
    """
    empty_value_display = 'Valor no ingresado'
    list_display = (
        'nombre',
        '_provincia'
    )

    list_filter = (
        'provincia',
    )

    def _provincia(self, obj):
        return obj.provincia.nombre

admin.site.register(Localidad, LocalidadAdmin)
