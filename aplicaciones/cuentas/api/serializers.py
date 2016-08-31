from rest_framework.serializers import (
    ModelSerializer,
)
from aplicaciones.base.models import (
    Donante,
    Direccion,
    RegistroDonacion,
)

from django.contrib.auth import get_user_model
from .token import (
    enviar_mail_activacion
)


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
        numeroDocumento = validated_data.get('numeroDocumento', None)
        tipoDocumento = validated_data.get('tipoDocumento', None)
        nacimiento = validated_data['nacimiento']
        telefono = validated_data.get('telefono', None)
        peso = validated_data['peso']
        altura = validated_data['altura']
        genero = validated_data['genero']
        grupoSanguineo = validated_data.get('grupoSanguineo', None)
        nacionalidad = validated_data.get('nacionalidad', None)

        # Obtención de datos del usuario
        usuario_data = validated_data.pop('usuario')
        usuario = User(**usuario_data)
        usuario.is_active = False
        # Seteo la password mediante el método set_password
        # para que la misma sea encriptada.
        usuario.set_password(usuario_data['password'])
        usuario.save()

        # Creación de la instancia de Donante
        donante_obj = Donante(
            usuario=usuario,
            numeroDocumento=numeroDocumento,
            tipoDocumento=tipoDocumento,
            nacimiento=nacimiento,
            telefono=telefono,
            peso=peso,
            altura=altura,
            genero=genero,
            grupoSanguineo=grupoSanguineo,
            nacionalidad=nacionalidad
        )

        # Obtención de los datos de la dirección
        direccion_data = validated_data.pop('direccion', None)
        if direccion_data is not None:
            direccion = Direccion(**direccion_data)
            direccion.save()

            donante_obj.direccion = direccion

        donante_obj.save()

        # Creación de instancia de Registro de donación asociada con la instancia de Donante
        RegistroDonacion.objects.create(donante=donante_obj)

        enviar_mail_activacion(usuario)

        return donante_obj
