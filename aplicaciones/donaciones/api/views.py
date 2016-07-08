from rest_framework.generics import CreateAPIView

from rest_framework.permissions import AllowAny

from aplicaciones.base.api.permissions import IsOwner

from rest_framework.parsers import FormParser, MultiPartParser, JSONParser

from aplicaciones.base.models import (
    RegistroDonacion,
    Donacion
    )

from .serializers import (
   DonacionAltaSerializer,
    )

class DonacionAltaAPI(CreateAPIView):
    permission_classes = [IsOwner]
    queryset = Donacion.objects.all()
    parser_classes = [FormParser, MultiPartParser, JSONParser]
    serializer_class = DonacionAltaSerializer