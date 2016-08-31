# coding=utf-8

from django.contrib import admin

from ..models import TipoDocumento


class TipoDocumentoAdmin(admin.ModelAdmin):
    """
    Especificación de la representación del tipo de documento en la interfaz de administración.
    """
    empty_value_display = 'Valor no ingresado'
    list_display = (
        'siglas',
        'descripcion'
    )


admin.site.register(TipoDocumento, TipoDocumentoAdmin)