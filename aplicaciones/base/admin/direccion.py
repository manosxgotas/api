from django.contrib import admin

from ..models import Direccion


class DireccionAdmin(admin.ModelAdmin):
    """
    Especificación de la representación de Dirección en la interfaz de administración.
    """
    empty_value_display = '--------'
    list_display = (
        'calle',
        'numero',
        '_provincia',
        'localidad',
        'piso',
        'numeroDepartamento',
        '_geoposicion'
    )

    def _provincia(self, obj):
        return obj.localidad.provincia

    def _geoposicion(self, obj):
        if obj.posicion:
            return 'Si'
        else:
            return 'No'

admin.site.register(Direccion, DireccionAdmin)
