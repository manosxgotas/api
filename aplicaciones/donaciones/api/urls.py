from django.conf.urls import url

from .views import (
    DonacionCreateAPI,
    DonacionUpdateAPI,
    DonacionDestroyAPI,
    DonacionInfoAPI
    )


urlpatterns = [

    url(r'^crear/$', DonacionCreateAPI.as_view() , name='crear-donacion'),
    url(r'^editar/(?P<id>\w+)$', DonacionUpdateAPI.as_view() , name='editar-donacion'),
    url(r'^eliminar/(?P<id>\w+)$', DonacionDestroyAPI.as_view() , name='eliminar-donacion'),
    url(r'^(?P<id>\w+)$', DonacionInfoAPI.as_view() , name='info-donacion'),
]