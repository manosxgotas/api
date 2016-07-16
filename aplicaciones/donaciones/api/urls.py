from django.conf.urls import url

from .views import (
    DonacionCreateAPI,
    DonacionUpdateAPI,
    DonacionDestroyAPI,
    DonacionInfoAPI,
    dias_proxima_donacion
    )


urlpatterns = [

    url(r'^crear/$', DonacionCreateAPI.as_view() , name='crear-donacion'),
    url(r'^editar/(?P<id>\w+)$', DonacionUpdateAPI.as_view() , name='editar-donacion'),
    url(r'^eliminar/(?P<id>\w+)$', DonacionDestroyAPI.as_view() , name='eliminar-donacion'),
    url(r'^(?P<id>\w+)$', DonacionInfoAPI.as_view() , name='info-donacion'),
    url(r'^proxima-donacion/(?P<usuario_id>\w+)$', dias_proxima_donacion , name='dias-proxima-donacion'),
]