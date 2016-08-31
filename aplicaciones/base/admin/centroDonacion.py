# coding=utf-8

from django.contrib import admin

from ..models import CentroDonacion, HorarioCentroDonacion, LugarDonacion


class HorarioCentroDonacionInline(admin.TabularInline):
    model = HorarioCentroDonacion


class CentroDonacionAdmin(admin.ModelAdmin):
    """
    Especificación de la representación del centro de
     donación en la interfaz de administración.
    """
    empty_value_display = 'Valor no ingresado'
    list_display = (
        'nombre',
        '_tipoCentro',
    )

    list_filter = (
        'tipo',
    )

    inlines = [
        HorarioCentroDonacionInline,
    ]

    def _tipoCentro(self, obj):
        return obj.tipo.nombre



admin.site.register(CentroDonacion, CentroDonacionAdmin)