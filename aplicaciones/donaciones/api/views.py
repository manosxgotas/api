import datetime

from rest_framework.generics import (
    CreateAPIView,
    UpdateAPIView,
    RetrieveAPIView
    )

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST
    )

from rest_framework.serializers import ValidationError

from rest_framework.mixins import (
        DestroyModelMixin
    )

from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.response import Response
from rest_framework.decorators import api_view

from aplicaciones.base.api.permissions import IsOwnerDonacion

from aplicaciones.base.models import (
    CodigoVerificacion,
    Donacion,
    EstadoDonacion,
    HistoricoEstadoDonacion,
    RegistroDonacion,
    DIAS_DONACION_POR_GENERO
    )

from .serializers import (
    create_update_destroy_donacion_serializer,
    DonacionSerializer,
    VerificarImagenDonacionSerializer,
    RegistroDonacionSerializer,
    ESTADO_VERIFICADA
    )


class DonacionCreateAPI(CreateAPIView):
    permission_classes = [IsOwnerDonacion]
    queryset = Donacion.objects.all()
    parser_classes = [FormParser, MultiPartParser, JSONParser]

    def get_serializer_class(self):
        usuario = self.request.user
        return create_update_destroy_donacion_serializer(
                usuario=usuario
            )


class DonacionUpdateAPI(UpdateAPIView):
    permission_classes = [IsOwnerDonacion]
    queryset = Donacion.objects.all()
    parser_classes = [FormParser, MultiPartParser, JSONParser]
    lookup_field = 'id'

    def get_serializer_class(self):
        usuario = self.request.user
        return create_update_destroy_donacion_serializer(
                usuario=usuario
            )


class DonacionDestroyAPI(RetrieveAPIView, DestroyModelMixin):
    permission_classes = [IsOwnerDonacion]
    queryset = Donacion.objects.all()
    lookup_field = 'id'

    def get_serializer_class(self):
        usuario = self.request.user
        return create_update_destroy_donacion_serializer(
                usuario=usuario
            )

    def delete(self, request, *args, **kwargs):
        donacion = self.get_object()
        if donacion.historicoEstados:
            ultimo_historico_donacion = donacion.historicoEstados.latest('inicio')
            ultimo_estado = ultimo_historico_donacion.estado.nombre
            if ultimo_estado.lower() == ESTADO_VERIFICADA:
                raise ValidationError('No puedes eliminar una donación que se encuentre verificada.')

        return self.destroy(request, *args, **kwargs)


class DonacionInfoAPI(RetrieveAPIView):
    permission_classes = [IsOwnerDonacion]
    queryset = Donacion.objects.all()
    serializer_class = DonacionSerializer
    lookup_field = 'id'


class VerificarImagenDonacionAPI(UpdateAPIView):
    queryset = Donacion.objects.all()
    parser_classes = [FormParser, MultiPartParser]
    serializer_class = VerificarImagenDonacionSerializer
    lookup_field = 'id'


class RegistroDonacionInfoAPI(RetrieveAPIView):
    serializer_class = RegistroDonacionSerializer
    queryset = RegistroDonacion.objects.all()

    def get_object(self):
        return self.request.user.donante.registro


@api_view(['GET'])
def dias_proxima_donacion(request):

    # Obtengo donante por id de usuario.
    donante = request.user.donante

    # Obtengo el listado de donaciones del donante ordenadas por fecha y hora.
    donaciones_donante = donante.registro.donaciones.order_by("fechaHora")

    # Si el donante posee donaciones
    if donaciones_donante:

        # Obtengo la fecha y hora de la última donación
        # realizada por el donante.
        ultima_donacion = donaciones_donante.last().fechaHora

        # Obtengo el género del donante.
        genero_donante = donante.genero

        # Calculo la diferencia de días entre la última donación
        # realizada por el donante y la fecha actual.
        dias_desde_ultima_donacion = datetime.datetime.now() - ultima_donacion

        # Dependiendo del sexo del donante obtengo la cantidad
        # de días necesarios para que el donante pueda realizar.
        # una nueva donación.
        dias_proxima_donacion = DIAS_DONACION_POR_GENERO[genero_donante] - dias_desde_ultima_donacion.days

        # Si la espera en días se cumplió, establezco la cantidad de días en 0.
        return Response({"dias": max(dias_proxima_donacion, 0)})

    # Si no posee donaciones retorno 0, es decir que está apto para donar.
    return Response({"dias": 0})


@api_view(['POST'])
def verificar_codigo_donacion(request, donacion_id):
    # Obtengo codigo ingresado
    codigo_ingresado = CodigoVerificacion.objects.filter(codigo=request.data['codigo'])

    # Si existe en la base de datos
    if codigo_ingresado.exists():
        donacion = Donacion.objects.get(id=donacion_id)

        # Verifico que la fecha de la donación sea posterior a la fecha
        # de emisión del código.
        if donacion.fechaHora.date() >= codigo_ingresado[0].fechaEmision:
            ultimo_historico_donacion = donacion.historicoEstados.last()

            # Compruebo que la donación no se encuentre verificada.
            if ultimo_historico_donacion.estado.nombre != 'Verificada':
                # Establezco fecha fin del último histórico de la donación
                ultimo_historico_donacion.fin = datetime.datetime.now()
                ultimo_historico_donacion.save()
                estado = EstadoDonacion.objects.get(nombre='Verificada')

                # Creo nuevo histórico
                HistoricoEstadoDonacion.objects.create(
                    inicio=datetime.datetime.now(),
                    estado=estado,
                    donacion=donacion
                    )

                # Borro código de la base de datos.
                codigo_ingresado.delete()

                return Response(
                    {"mensaje": '¡Verificación exitosa!'},
                    status=HTTP_200_OK
                    )

            else:
                return Response(
                    {"mensaje": 'Esta donación ya ha sido verificada anteriormente.'},
                    status=HTTP_400_BAD_REQUEST
                    )

        else:
            return Response(
                {"mensaje": 'No puedes utilizar el código introducido debido a que la donación es anterior a la emisión del mismo.'},
                status=HTTP_400_BAD_REQUEST
                )

    return Response(
        {"mensaje": 'El código ingresado es incorrecto o ya ha sido utilizado.'},
        status=HTTP_400_BAD_REQUEST
        )
