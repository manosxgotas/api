# coding=utf-8

from django.contrib import admin

from ..models import Nacionalidad


class NacionalidadAdmin(admin.ModelAdmin):
    """
    Especificación de la representación de la nacionalidad en la interfaz de administración.
    """
    empty_value_display = 'Valor no ingresado'
    list_display = (
        'nombre',
    )




admin.site.register(Nacionalidad, NacionalidadAdmin)