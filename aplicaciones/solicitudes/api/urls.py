from django.conf.urls import url

from .views import (
    SolicitudDonacionCreateAPI,
    SolicitudDonacionInfoAPI,
    TipoSolicitudAPI,
    SolicitudesInfoAPI,
    SolicitudesDonanteListAPI,
    SolicitudDonacionDeleteAPI
    )

urlpatterns = [
    url(
        r'^crear/$',
        SolicitudDonacionCreateAPI.as_view(),
        name='crear-solicitud'
    ),

    url(
        r'^(?P<id>\w+)$',
        SolicitudDonacionInfoAPI.as_view(),
        name='detalle-solicitud'
    ),

    url(
        r'^listado-tipos-solicitudes/$',
        TipoSolicitudAPI.as_view(),
        name='listado-tipos-solicitudes'
    ),

    url(
        r'^listado-solicitudes/$',
        SolicitudesInfoAPI.as_view(),
        name='listado-solicitudes'
    ),
    url(
        r'^listado-solicitudes-donante/$',
        SolicitudesDonanteListAPI.as_view(),
        name='listado-solicitudes-donante'
    ),
    url(
        r'^eliminar/(?P<id>\w+)$',
        SolicitudDonacionDeleteAPI.as_view(),
        name='eliminar-solicitud'
    ),
]
