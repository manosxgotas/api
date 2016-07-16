import datetime

from rest_framework.generics import (
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
    RetrieveAPIView
    )

from rest_framework.permissions import AllowAny

from aplicaciones.base.api.permissions import IsOwnerDonacion

from rest_framework.parsers import FormParser, MultiPartParser, JSONParser

from rest_framework.response import Response
from rest_framework.decorators import api_view

from aplicaciones.base.models import (
    RegistroDonacion,
    Donante,
    Donacion,
    DIAS_DONACION_POR_GENERO
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


@api_view(['GET'])
def dias_proxima_donacion(request, usuario_id):

    # Obtengo donante por id de usuario.
    donante = Donante.objects.get(usuario__id=usuario_id)

    # Obtengo el listado de donaciones del donante ordenadas por fecha y hora.
    donaciones_donante = donante.registro.donaciones.order_by("fechaHora")

    # Si el donante posee donaciones
    if donaciones_donante:

        # Obtengo la fecha y hora de la última donación realizada por el donante.
        ultima_donacion = donaciones_donante.last().fechaHora

        # Obtengo el género del donante.
        genero_donante = donante.genero

        # Calculo la diferencia de días entre la última donación realizada por el donante y la fecha actual.
        dias_desde_ultima_donacion = datetime.datetime.now() - ultima_donacion

        # Dependiendo del sexo del donante obtengo la cantidad de días necesarios para que el donante pueda realizar una nueva donación.
        dias_proxima_donacion = DIAS_DONACION_POR_GENERO[genero_donante] - dias_desde_ultima_donacion.days

        # Si la espera en días se cumplió, establezco la cantidad de días en 0.
        return Response({"dias": max(dias_proxima_donacion, 0)})

    # Si no posee donaciones retorno 0, es decir que está apto para donar.
    return Response({"dias": 0})