import datetime
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.decorators import (
    api_view,
    permission_classes
    )
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST
    )
from aplicaciones.base.models import (
    Donante,
    )
from .serializers import (
    DonanteRegistroSerializer,
    )

from .token import confirmar_token


class DonanteRegistroAPI(CreateAPIView):
    permission_classes = [AllowAny]
    queryset = Donante.objects.all()
    serializer_class = DonanteRegistroSerializer


@api_view(['POST', 'GET'])
@permission_classes((AllowAny, ))
def activar_cuenta(request, token=None):
    '''
    Activación de cuenta mediante acceso a link (GET) o mediante
    clave (POST), en ambos casos se comprueba que el link/clave no
    se encuentren vencidos y que el usuario no se encuentre ya
    activo.
    '''
    Usuario = get_user_model()
    if request.method == 'GET':
        key = confirmar_token(token, url=True)
    else:
        key = confirmar_token(request.data['clave'])

    if key is False:
        return Response(
            {"mensaje": 'El link de confirmación es inválido o ha vencido.'},
            status=HTTP_400_BAD_REQUEST
        )
    else:
        if request.method == 'GET':
            usuario = get_object_or_404(Usuario, email=key)
        else:
            usuario = get_object_or_404(Usuario, id=key)
        if usuario.is_active:
            return Response(
                {"mensaje": 'Esta cuenta ya se encuentra activada.'},
                status=HTTP_400_BAD_REQUEST
            )
        else:
            usuario.is_active = True
            usuario.save()
            return Response(
                {"mensaje": 'Se ha activado correctamente tu cuenta de registro. ¡Gracias!'},
                status=HTTP_200_OK
            )
