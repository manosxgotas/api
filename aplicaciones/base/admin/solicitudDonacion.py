# coding=utf-8

from django.contrib import admin

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
        'estado',
        'centroDonacion',
        'paciente',
    )

    list_filter = (
        'estado',
        'tipo',
        'centroDonacion'
    )

    inlines = [
            ImagenSolicitudDonacionInline
        ]

admin.site.register(SolicitudDonacion, SolicitudDonacionAdmin)
