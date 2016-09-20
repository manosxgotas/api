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
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND
    )
from aplicaciones.base.models import (
    Donante,
    )

from .token import (
    confirmar_token,
    enviar_mail_reiniciar_password
    )

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView


class FacebookLogin(SocialLoginView):
    permission_classes = [AllowAny]
    adapter_class = FacebookOAuth2Adapter


class GoogleLogin(SocialLoginView):
    permission_classes = [AllowAny]
    adapter_class = GoogleOAuth2Adapter

Usuario = get_user_model()


@api_view(['POST', 'GET'])
@permission_classes((AllowAny, ))
def activar_cuenta(request, token=None):
    '''
    Activación de cuenta mediante acceso a link (GET) o mediante
    clave (POST), en ambos casos se comprueba que el link/clave no
    se encuentren vencidos y que el usuario no se encuentre ya
    activo.
    '''
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


@api_view(['POST'])
@permission_classes((AllowAny, ))
def reset_pass_request(request):

    usuario = Usuario.objects.filter(email=request.data['email'])
    if usuario.exists():
        enviar_mail_reiniciar_password(usuario[0])
        return Response(
                {"mensaje": 'Pronto recibirás un correo electrónico con las instrucciones para recuperar tu contraseña.'},
                status=HTTP_200_OK
            )
    else:
        return Response(
                {"mensaje": 'El correo ingresado no pertenece a ningún usuario, ¿te has registrado anteriormente?'},
                status=HTTP_400_BAD_REQUEST
            )


@api_view(['POST', 'GET'])
@permission_classes((AllowAny, ))
def reset_pass(request, token=None):
    if request.method == 'GET':
        email = confirmar_token(token, url=True)
    else:
        email = confirmar_token(request.data['token'], url=True)

    if email is False:
        return Response(
                    {"mensaje": 'El link de reinicio de constraseña es inválido o ha vencido.'},
                    status=HTTP_404_NOT_FOUND
                )
    else:
        if request.method == 'POST':
            usuario = get_object_or_404(Usuario, email=email)
            if request.data['password'] != request.data['password2']:
                return Response(
                        {"mensaje": 'Las contraseñas no coinciden, vuelve a intentar.'},
                        status=HTTP_400_BAD_REQUEST
                    )
            else:
                usuario.set_password(request.data['password'])
                usuario.save()
                return Response(
                        {"mensaje": '¡Tu contraseña ha sido reiniciada exitosamente!'},
                        status=HTTP_200_OK
                    )
        else:
            return Response(
                    {"mensaje": 'El link de reinicio de constraseña es correcto.'},
                    status=HTTP_200_OK
                )
