from rest_framework.permissions import AllowAny
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    ListAPIView,
    RetrieveDestroyAPIView
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
    SolicitudesDonanteInfoSerializer,
    EliminarSolicitudSerializer,
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
 
class SolicitudesDonanteInfoAPI(ListAPIView):
    queryset = SolicitudDonacion.objects.all()
    serializer_class = SolicitudesDonanteInfoSerializer
    
    def get_queryset(self):
        donanteID = self.kwargs['donante']
        return SolicitudDonacion.objects.filter(donante=donanteID)


class EliminarSolicitudInfoAPI(RetrieveDestroyAPIView):
    queryset = SolicitudDonacion.objects.all()
    serializer_class = EliminarSolicitudSerializer
    lookup_field = 'id'