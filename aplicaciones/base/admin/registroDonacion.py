# coding=utf-8

from django.contrib import admin

from ..models import RegistroDonacion


class RegistroDonacionInline(admin.TabularInline):
    model = RegistroDonacion