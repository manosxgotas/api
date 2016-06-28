from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    )

from aplicaciones.base.api.permissions import IsOwner

from rest_framework.views import APIView
from rest_framework.decorators import parser_classes
from rest_framework.parsers import FormParser, MultiPartParser

from aplicaciones.base.models import (
    Donante,
    )

from .serializers import (
    DonantePerfilSerializer,
    DonanteUpdateSerializer,
    DonanteAvatarSerializer,
    )

class DonantePerfilAPI(RetrieveAPIView):
    permission_classes = [IsOwner]
    serializer_class = DonantePerfilSerializer
    queryset = Donante.objects.all()
    lookup_field = 'usuario_id'

class DonanteUpdateAPI(UpdateAPIView):
    permission_classes = [IsOwner]
    serializer_class = DonanteUpdateSerializer
    queryset = Donante.objects.all()
    lookup_field = 'usuario_id'

class DonanteUpdateAvatarAPI(UpdateAPIView):
    permission_classes = [IsOwner]
    parser_classes = [FormParser, MultiPartParser]
    serializer_class = DonanteAvatarSerializer
    queryset = Donante.objects.all()
    lookup_field = 'usuario_id'