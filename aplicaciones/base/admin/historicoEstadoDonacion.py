# coding=utf-8

from django.contrib import admin

from ..models import HistoricoEstadoDonacion


class HistoricoEstadoDonacionInline(admin.TabularInline):
    model = HistoricoEstadoDonacion
    readonly_fields = (
        'inicio',
        'fin',
        'estado'
    )
    can_delete = False
