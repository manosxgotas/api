from django.conf.urls import include, url

from .views import (
    ProvinciaListAPI,
    LocalidadListAPI,
    )

urlpatterns = [
    url(r'^listado-provincias/$', ProvinciaListAPI.as_view() , name='listado-provincias'),
    url(r'^localidades/provincia/(?P<provincia_id>\w+)$', LocalidadListAPI.as_view() , name='listado-localidades'),
]