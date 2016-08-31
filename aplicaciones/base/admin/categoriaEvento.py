# coding=utf-8

from django.contrib import admin

from ..models import CategoriaEvento


class CategoriaEventoAdmin(admin.ModelAdmin):
    """
    Especificación de la representación de la categoria de eventos en la interfaz de administración.
    """
    empty_value_display = 'Valor no ingresado'
    list_display = (
        'nombre',
        'descripcion'
    )


admin.site.register(CategoriaEvento, CategoriaEventoAdmin)