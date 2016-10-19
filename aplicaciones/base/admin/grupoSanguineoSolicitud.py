# coding=utf-8

from django.contrib import admin

from ..models import GrupoSanguineoSolicitud


class GrupoSanguineoSolicitudInline(admin.TabularInline):
    model = GrupoSanguineoSolicitud
