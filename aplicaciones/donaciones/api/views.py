from rest_framework.generics import CreateAPIView

from rest_framework.permissions import AllowAny

from aplicaciones.base.api.permissions import IsOwner

from aplicaciones.base.models import (
    RegistroDonacion,
    Donacion
    )

from .serializers import (
   DonacionSerializer,
    )

class DonacionAltaAPI(CreateAPIView):
    permission_classes = [IsOwner]
    queryset = Donacion.objects.all()
    serializer_class = DonacionSerializer