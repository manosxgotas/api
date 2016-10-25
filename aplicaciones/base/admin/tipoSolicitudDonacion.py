# coding=utf-8

from django.contrib import admin

from ..models import TipoSolicitudDonacion


class TipoSolicitudDonacionAdmin(admin.ModelAdmin):
    """
    Especificación de la representación del tipo de solicitud de donacion en la interfaz de administración.
    """
    empty_value_display = '--------'
    list_display = (
        'nombre',
        'descripcion'
    )


admin.site.register(TipoSolicitudDonacion, TipoSolicitudDonacionAdmin)
