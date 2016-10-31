from rest_framework.permissions import AllowAny
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    ListAPIView,
    DestroyAPIView
    )

from aplicaciones.base.models import (
    SolicitudDonacion,
    TipoSolicitudDonacion,
)

from .serializers import (
    create_solicitud_donacion_serializer,
    SolicitudDonacionInfoSerializer,
    TipoSolicitudSerializer,
    SolicitudDonacionListadoSerializer
)

from aplicaciones.base.api.permissions import IsOwnerSolicitud


class SolicitudDonacionCreateAPI(CreateAPIView):
    queryset = SolicitudDonacion.objects.all()
    parser_classes = [FormParser, MultiPartParser, JSONParser]

    def get_serializer_class(self):
        usuario = self.request.user
        return create_solicitud_donacion_serializer(
                usuario=usuario
            )


class SolicitudDonacionInfoAPI(RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = SolicitudDonacion.objects.all()
    serializer_class = SolicitudDonacionInfoSerializer
    lookup_field = 'id'


class TipoSolicitudAPI(ListAPIView):
    queryset = TipoSolicitudDonacion.objects.all()
    serializer_class = TipoSolicitudSerializer


class SolicitudesInfoAPI(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = SolicitudDonacionListadoSerializer
    queryset = SolicitudDonacion.objects.all()


class SolicitudesDonanteListAPI(ListAPIView):
    queryset = SolicitudDonacion.objects.all()
    serializer_class = SolicitudDonacionListadoSerializer

    def get_queryset(self):
        donante = self.request.user.donante
        return SolicitudDonacion.objects.filter(donante=donante)


class SolicitudDonacionDeleteAPI(DestroyAPIView):
    permission_classes = [IsOwnerSolicitud]
    queryset = SolicitudDonacion.objects.all()
    serializer_class = SolicitudDonacionInfoSerializer
    lookup_field = 'id'
