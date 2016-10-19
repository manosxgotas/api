# coding=utf-8

from django.contrib import admin
from .grupoSanguineoSolicitud import GrupoSanguineoSolicitudInline

from ..models import (
    SolicitudDonacion,
    ImagenSolicitudDonacion
    )


class ImagenSolicitudDonacionInline(admin.TabularInline):
    model = ImagenSolicitudDonacion


class SolicitudDonacionAdmin(admin.ModelAdmin):
    """
    Especificación de la representación de la solicitud de
     donación en la interfaz de administración.
    """
    empty_value_display = 'Valor no ingresado'
    list_display = (
        'id',
        'titulo',
        'fechaPublicacion',
        'tipo',
        'centroDonacion',
        'paciente',
    )

    list_filter = (
        'tipo',
        'centroDonacion'
    )

    inlines = [
            ImagenSolicitudDonacionInline,
            GrupoSanguineoSolicitudInline
        ]

admin.site.register(SolicitudDonacion, SolicitudDonacionAdmin)
