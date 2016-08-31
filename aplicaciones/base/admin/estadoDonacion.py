# coding=utf-8

from django.contrib import admin

from ..models import EstadoDonacion


class EstadoDonacionAdmin(admin.ModelAdmin):
    """
    Especificación de la representación del estado de la
     donación en la interfaz de administración.
    """
    empty_value_display = 'Valor no ingresado'
    list_display = (
        'nombre',
        'descripcion'
    )


admin.site.register(EstadoDonacion, EstadoDonacionAdmin)