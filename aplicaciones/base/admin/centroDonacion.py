# coding=utf-8

from django.contrib import admin

from ..models import (
    CentroDonacion,
    HorarioCentroDonacion,
    LugarDonacion
)


class HorarioCentroDonacionInline(admin.TabularInline):
    model = HorarioCentroDonacion


class CentroDonacionAdmin(admin.ModelAdmin):
    """
    Especificación de la representación del centro de
     donación en la interfaz de administración.
    """
    empty_value_display = '--------'
    list_display = (
        'nombre',
        'tipo',
        'activo'
    )

    list_filter = (
        'tipo',
        'activo'
    )

    inlines = [
        HorarioCentroDonacionInline,
    ]

admin.site.register(CentroDonacion, CentroDonacionAdmin)
