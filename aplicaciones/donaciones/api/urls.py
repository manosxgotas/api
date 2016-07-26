from django.conf.urls import url

from .views import (
    DonacionCreateAPI,
    DonacionUpdateAPI,
    DonacionDestroyAPI,
    DonacionInfoAPI,
    VerificarImagenDonacionAPI,
    dias_proxima_donacion,
    verificar_codigo_donacion
    )

urlpatterns = [

    url(
        r'^crear/$',
        DonacionCreateAPI.as_view(),
        name='crear-donacion'
        ),

    url(
        r'^editar/(?P<id>\w+)$',
        DonacionUpdateAPI.as_view(),
        name='editar-donacion'
        ),

    url(
        r'^eliminar/(?P<id>\w+)$',
        DonacionDestroyAPI.as_view(),
        name='eliminar-donacion'
        ),

    url(
        r'^(?P<id>\w+)$',
        DonacionInfoAPI.as_view(),
        name='info-donacion'
        ),

    url(
        r'^proxima-donacion/(?P<usuario_id>\w+)$',
        dias_proxima_donacion,
        name='dias-proxima-donacion'
        ),

    url(
        r'^verificar-codigo/(?P<donacion_id>\w+)$',
        verificar_codigo_donacion,
        name='verificar-codigo-donacion'
        ),

    url(
        r'^verificar-imagen/(?P<donacion_id>\w+)$',
        VerificarImagenDonacionAPI.as_view(),
        name='verificar-imagen-donacion'
        )
    ]
