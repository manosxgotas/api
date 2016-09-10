from .serializers import (
    CentroDonacionSerializer,
    DonanteSerializer,
    EventoSerializer,
    GrupoSanguineoSerializer,
    NacionalidadSerializer,
    TipoDocumentoSerializer,
    )
from aplicaciones.base.models import (
    CentroDonacion,
    Donante,
    GrupoSanguineo,
    Evento,
    Nacionalidad,
    TipoDocumento
    )
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny


class CentroDonacionListAPI(ListAPIView):
    queryset = CentroDonacion.objects.all()
    serializer_class = CentroDonacionSerializer


class DonanteListAPI(ListAPIView):
    queryset = Donante.objects.all()
    serializer_class = DonanteSerializer


class EventoInfoAPI(RetrieveAPIView):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    lookup_field = 'id'


class EventoListAPI(ListAPIView):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer


class GrupoSanguineoListAPI(ListAPIView):
    permission_classes = [AllowAny]
    queryset = GrupoSanguineo.objects.all()
    serializer_class = GrupoSanguineoSerializer


class NacionalidadListAPI(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Nacionalidad.objects.all()
    serializer_class = NacionalidadSerializer


class TipoDocumentoListAPI(ListAPIView):
    permission_classes = [AllowAny]
    queryset = TipoDocumento.objects.all()
    serializer_class = TipoDocumentoSerializer

