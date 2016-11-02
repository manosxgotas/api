# coding=utf-8

from django.contrib import admin

from ..models import Donante


class DonanteAdmin(admin.ModelAdmin):
    """
    Especificación de la representación de Donante en la interfaz de administración.
    """
    empty_value_display = '--------'
    list_display = (
        'usuario',
        '_nombre',
        'genero',
        'grupoSanguineo',
        'nacionalidad',
        'tipoDocumento',
        'numeroDocumento'
    )

    list_filter = [
        'genero',
        'grupoSanguineo',
        'nacionalidad'
    ]

    def _nombre(self, obj):
        return obj.usuario.get_full_name()

admin.site.register(Donante, DonanteAdmin)
