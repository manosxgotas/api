# coding=utf-8

from django.contrib import admin

from ..models import TipoCentroDonacion


class TipoCentroDonacionAdmin(admin.ModelAdmin):
    """
    Especificación de la representación del tipo del centro de donación en la interfaz de administración.
    """
    empty_value_display = 'Valor no ingresado'
    list_display = (
        'nombre',
        'descripcion'
    )


admin.site.register(TipoCentroDonacion, TipoCentroDonacionAdmin)