# coding=utf-8

from django.contrib import admin

from .registroDonacion import RegistroDonacionInline
from ..models import Donante

class DonanteAdmin(admin.ModelAdmin):
    """
    Especificación de la representación de Donante en la interfaz de administración.
    """
    empty_value_display = 'Valor no ingresado'
    list_display = (
        'usuario',
        '_nombre',
        '_tipoDocumento',
        '_dni'
    )

    inlines = [
        RegistroDonacionInline,
    ]


    def _nombre (self, obj):
        return obj.usuario.get_full_name()

    """
    Comruebación de numero y tipo de DNI para el usuario
    """

    def _tipoDocumento (self, obj):
        if obj.tipoDocumento:
            s = obj.tipoDocumento.siglas
        else:
            s = 'No se especifica valor'
        return s

    def _dni (self, obj):
        if obj.numeroDocumento:
            s = obj.numeroDocumento
        else:
            s = 'No se especifica valor'
        return s

admin.site.register(Donante, DonanteAdmin)