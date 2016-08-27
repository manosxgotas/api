import datetime

from rest_framework.serializers import (
    ModelSerializer,
    ValidationError,
    )
from aplicaciones.base.models import (
    Donante,
    Direccion,
    RegistroDonacion,
    )

from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.template import loader
from .token import generar_token_confirmacion

class DireccionRegistroSerializer(ModelSerializer):

    class Meta:
        model = Direccion
        fields = [
        'calle',
        'numero',
        'piso',
        'numeroDepartamento',
        'localidad',
        ]

User = get_user_model()


class UsuarioRegistroSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
        ]

    extra_kwargs = {'password': {'write_only': True}}


class DonanteRegistroSerializer(ModelSerializer):
    usuario = UsuarioRegistroSerializer()
    direccion = DireccionRegistroSerializer()

    class Meta:
        model = Donante
        fields = [
        'usuario',
        'numeroDocumento',
        'tipoDocumento',
        'nacimiento',
        'telefono',
        'peso',
        'altura',
        'genero',
        'grupoSanguineo',
        'direccion',
        'nacionalidad'
        ]

    def create(self, validated_data):

        # Obtención de datos del donante
        numeroDocumento = validated_data['numeroDocumento']
        tipoDocumento = validated_data['tipoDocumento']
        nacimiento = validated_data['nacimiento']
        telefono = validated_data['telefono']
        peso = validated_data['peso']
        altura = validated_data['altura']
        genero = validated_data['genero']
        grupoSanguineo = validated_data.get('grupoSanguineo', None)
        nacionalidad = validated_data['nacionalidad']

        # Obtención de datos del usuario
        usuario_data = validated_data.pop('usuario')
        usuario = User(**usuario_data)
        usuario.is_active = False
        # Seteo la password mediante el método set_password para que la misma sea encriptada
        usuario.set_password(usuario_data['password'])
        usuario.save()

        # Obtención de los datos de la dirección
        direccion_data = validated_data.pop('direccion')
        direccion = Direccion(**direccion_data)
        direccion.save()

        # Creación de la instancia de Donante
        donante_obj = Donante.objects.create(
            usuario = usuario,
            claveActivacion = claveActivacion,
            vencimientoClaveActivacion = vencimientoClaveActivacion,
            numeroDocumento = numeroDocumento,
            tipoDocumento = tipoDocumento,
            nacimiento = nacimiento,
            telefono = telefono,
            peso = peso,
            altura = altura,
            genero = genero,
            grupoSanguineo = grupoSanguineo,
            direccion = direccion,
            nacionalidad = nacionalidad
            )

        # Creación de instancia de Registro de donación asociada con la instancia de Donante
        RegistroDonacion.objects.create(donante=donante_obj)

        # Se genera token con email del usuario.
        token = generar_token_confirmacion(usuario.email)
        # Creación de URL de confirmación
        confirm_url = reverse('base:cuentas:activar-cuenta-link', kwargs={'token': token})

        # Obtención de templates html y txt de emails.
        htmly = loader.get_template('emails/html/confirmar_cuenta.html')
        text = loader.get_template('emails/txt/confirmar_cuenta.txt')

        # Definición de variables de contexto
        variables = {
            'usuario': usuario,
            'confirm_url': confirm_url,
            'clave': claveActivacion
            }
        html_content = htmly.render(variables)
        text_content = text.render(variables)

        # Creación y envío de email.
        msg = EmailMultiAlternatives(
            'Bienvenido a Manos por gotas',
            text_content,
            to=[usuario.email]
            )

        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return donante_obj