import datetime
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser, FileUploadParser
from rest_framework.generics import (
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
    RetrieveAPIView,
    ListAPIView
    )

from aplicaciones.base.models import (
	SolicitudDonacion,
	TipoSolicitudDonacion,
	Paciente,
	GrupoSanguineoSolicitud

	)
from .serializers import (
	SolicitudDonacionCreateSerializer,
	SolicitudDonacionInfoSerializer,
	TipoSolicitudSerializer,
	PacienteCreateSerializer,
	SolicitudDonacionListadoSerializer,
	GrupoSanguineoSolicitudSerializer,
	PacienteInfoSerializer

	)

class SolicitudDonacionCreateAPI(CreateAPIView):
	permissions_class = [IsAuthenticatedOrReadOnly]
	serializer_class = SolicitudDonacionCreateSerializer	
	queryset = SolicitudDonacion.objects.all()
	parser_classes = [FormParser, MultiPartParser, JSONParser]

class SolicitudDonacionInfoAPI(RetrieveAPIView):
	queryset = SolicitudDonacion.objects.all()
	serializer_class = SolicitudDonacionInfoSerializer
	lookup_field = 'id'

class TipoSolicitudAPI(ListAPIView):
    permission_classes = [AllowAny]
    queryset = TipoSolicitudDonacion.objects.all()
    serializer_class = TipoSolicitudSerializer

class SolicitudDonacionCreateAPI(CreateAPIView):
	permissions_class = [IsAuthenticatedOrReadOnly]
	serializer_class = SolicitudDonacionCreateSerializer	
	queryset = SolicitudDonacion.objects.all()
	parser_classes = [FormParser, MultiPartParser, JSONParser]

class SolicitudesInfoAPI(ListAPIView):
	permissions_class = [IsAuthenticatedOrReadOnly]
	serializer_class = SolicitudDonacionListadoSerializer
	queryset = SolicitudDonacion.objects.all()

class PacienteCreateAPI(CreateAPIView):
	permissions_class = [IsAuthenticatedOrReadOnly]
	serializer_class = PacienteCreateSerializer	
	queryset = SolicitudDonacion.objects.all()
	parser_classes = [FormParser, MultiPartParser, JSONParser]
