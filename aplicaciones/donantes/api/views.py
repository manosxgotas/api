from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    )

from aplicaciones.base.api.permissions import IsOwner

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from django.contrib.auth import get_user_model

from aplicaciones.base.models import (
    Donante,
    )

from .serializers import (
    DonantePerfilSerializer,
    DonanteUpdateSerializer,
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