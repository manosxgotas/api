# coding=utf-8

from django.contrib import admin

from ..models import VerificacionDonacion


class VerificacionDonacionAdmin(admin.ModelAdmin):
    """
    Especificación de la representación de la verificación de la
     donación en la interfaz de administración.
    """
    empty_value_display = 'Valor no ingresado'
    list_display = (
        'id',
        'imagen',
    )

admin.site.register(VerificacionDonacion, VerificacionDonacionAdmin)