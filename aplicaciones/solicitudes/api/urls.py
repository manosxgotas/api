from django.conf.urls import url

from .views import (
	SolicitudDonacionCreateAPI,
	SolicitudDonacionInfoAPI,
	TipoSolicitudAPI,
	PacienteCreateAPI
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
        name='info-solicitud'
        ),

	url(
		r'^listado-tipos-solicitudes/$', 
		TipoSolicitudAPI.as_view(), 
		name='listado-tipos-solicitudes'
		),

	url(
		r'^crear-paciente/$',
        PacienteCreateAPI.as_view(),
        name='crear-paciente'
		),
]