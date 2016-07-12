from rest_framework.generics import (
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
    RetrieveAPIView
    )

from rest_framework.permissions import AllowAny

from aplicaciones.base.api.permissions import IsOwnerDonacion

from rest_framework.parsers import FormParser, MultiPartParser, JSONParser

from aplicaciones.base.models import (
    RegistroDonacion,
    Donacion
    )

from .serializers import (
    DonacionCreateSerializer,
    DonacionUpdateSerializer,
    )

class DonacionCreateAPI(CreateAPIView):
    permission_classes = [IsOwnerDonacion]
    queryset = Donacion.objects.all()
    parser_classes = [FormParser, MultiPartParser, JSONParser]
    serializer_class = DonacionCreateSerializer

class DonacionUpdateAPI(UpdateAPIView):
    permission_classes = [IsOwnerDonacion]
    queryset = Donacion.objects.all()
    serializer_class = DonacionUpdateSerializer
    lookup_field = 'id'

class DonacionDestroyAPI(DestroyAPIView):
    permission_classes = [IsOwnerDonacion]
    queryset = Donacion.objects.all()
    serializer_class = DonacionCreateSerializer
    lookup_field = 'id'

class DonacionInfoAPI(RetrieveAPIView):
    permission_classes = [IsOwnerDonacion]
    queryset = Donacion.objects.all()
    serializer_class = DonacionCreateSerializer
    lookup_field = 'id'