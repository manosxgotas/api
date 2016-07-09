from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView
    )

from rest_framework.permissions import AllowAny

from aplicaciones.base.api.permissions import IsOwnerDonacion

from rest_framework.parsers import FormParser, MultiPartParser, JSONParser

from aplicaciones.base.models import (
    RegistroDonacion,
    Donacion
    )

from .serializers import (
    DonacionABMSerializer,
    )

class DonacionAltaAPI(CreateAPIView):
    permission_classes = [IsOwnerDonacion]
    queryset = Donacion.objects.all()
    parser_classes = [FormParser, MultiPartParser, JSONParser]
    serializer_class = DonacionABMSerializer

class DonacionEliminarAPI(DestroyAPIView):
    permission_classes = [IsOwnerDonacion]
    queryset = Donacion.objects.all()
    serializer_class = DonacionABMSerializer
    lookup_field = 'id'