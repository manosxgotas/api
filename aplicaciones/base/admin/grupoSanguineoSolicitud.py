# coding=utf-8

from django.contrib import admin

from ..models import GrupoSanguineoSolicitud


class GrupoSanguineoSolicitudAdmin(admin.ModelAdmin):
    """
    Especificación de la representación del grupo sanguine de
    la solicitud de donación en la interfaz de administración.
    """
    empty_value_display = 'Valor no ingresado'
    list_display = (
        'id',
        'solicitud',
        'grupoSanguineo'
    )

admin.site.register(GrupoSanguineoSolicitud, GrupoSanguineoSolicitudAdmin)