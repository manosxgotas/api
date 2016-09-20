from rest_framework.generics import (
    RetrieveAPIView,
    UpdateAPIView,
    )

from aplicaciones.base.api.permissions import IsOwner

from rest_framework.parsers import FormParser, MultiPartParser

from aplicaciones.base.models import (
    Donante,
    )

from .serializers import (
    DonantePerfilSerializer,
    DonanteUpdateSerializer,
    DonanteUpdateDireccionSerializer,
    DonanteUpdateAvatarSerializer,
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


class DonanteUpdateDireccionAPI(UpdateAPIView):
    permission_classes = [IsOwner]
    serializer_class = DonanteUpdateDireccionSerializer
    queryset = Donante.objects.all()
    lookup_field = 'usuario_id'


class DonanteUpdateAvatarAPI(UpdateAPIView):
    permission_classes = [IsOwner]
    parser_classes = [FormParser, MultiPartParser]
    serializer_class = DonanteUpdateAvatarSerializer
    queryset = Donante.objects.all()
    lookup_field = 'usuario_id'
