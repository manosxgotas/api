# coding=utf-8

from django.contrib import admin

from ..models import GrupoSanguineo


class GrupoSanguineoAdmin(admin.ModelAdmin):
    """
    Especificación de la representación de los grupos sanguineos en la interfaz de administración.
    """
    empty_value_display = 'Valor no ingresado'
    list_display = (
        'nombre',
    )

admin.site.register(GrupoSanguineo, GrupoSanguineoAdmin)