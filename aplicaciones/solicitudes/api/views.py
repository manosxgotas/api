from rest_framework.permissions import AllowAny
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    ListAPIView
    )

from aplicaciones.base.models import (
    SolicitudDonacion,
    TipoSolicitudDonacion,
)

from .serializers import (
    create_solicitud_donacion_serializer,
    SolicitudDonacionInfoSerializer,
    TipoSolicitudSerializer,
    SolicitudDonacionListadoSerializer,
)


class SolicitudDonacionCreateAPI(CreateAPIView):
    queryset = SolicitudDonacion.objects.all()
    parser_classes = [FormParser, MultiPartParser, JSONParser]

    def get_serializer_class(self):
        usuario = self.request.user
        return create_solicitud_donacion_serializer(
                usuario=usuario
            )


class SolicitudDonacionInfoAPI(RetrieveAPIView):
    queryset = SolicitudDonacion.objects.all()
    serializer_class = SolicitudDonacionInfoSerializer
    lookup_field = 'id'


class TipoSolicitudAPI(ListAPIView):
    permission_classes = [AllowAny]
    queryset = TipoSolicitudDonacion.objects.all()
    serializer_class = TipoSolicitudSerializer


class SolicitudesInfoAPI(ListAPIView):
    permissions_class = [AllowAny]
    serializer_class = SolicitudDonacionListadoSerializer
    queryset = SolicitudDonacion.objects.all()
