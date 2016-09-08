# coding=utf-8

from django.contrib import admin

from ..models import Paciente


class PacienteAdmin(admin.ModelAdmin):
    """
    Especificación de la representación del paciente en la interfaz de administración.
    """
    empty_value_display = 'Valor no ingresado'
    list_display = (
        'nombre',
        'apellido',
        'email'
    )

admin.site.register(Paciente, PacienteAdmin)
