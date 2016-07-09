from django.conf.urls import url

from .views import (
    DonacionAltaAPI,
    DonacionEliminarAPI
    )


urlpatterns = [
    url(r'^crear/$', DonacionAltaAPI.as_view() , name='alta-donacion'),
    url(r'^eliminar/(?P<id>\w+)$', DonacionEliminarAPI.as_view() , name='eliminar-donacion'),
]