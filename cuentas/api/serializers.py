from rest_framework.serializers import (
    ModelSerializer,
    EmailField,
    ValidationError,
    CharField,
    ModelField,
    )
from app.models import (
    Donante, 
    Direccion,
    RegistroDonacion,
    GENEROS,
    )

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils.text import slugify


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
        'nacimiento',
        'telefono',
        'peso',
        'altura',
        'genero',
        'grupoSanguineo',
        'direccion',
        ]

    def create(self, validated_data):
        nacimiento = validated_data['nacimiento']
        telefono = validated_data['telefono']
        peso = validated_data['peso']
        altura = validated_data['altura']
        genero = validated_data['genero']
        slug = slugify(validated_data['usuario']['username'])
        
        grupoSanguineo = validated_data['grupoSanguineo']

        usuario_data = validated_data.pop('usuario')
        usuario = User(**usuario_data)
        usuario.set_password(usuario_data['password'])
        usuario.save()
        
        direccion_data = validated_data.pop('direccion')
        direccion = Direccion(**direccion_data)
        direccion.save()

        donante_obj = Donante.objects.create(
            usuario = usuario,
            slug = slug,
            nacimiento = nacimiento,
            telefono = telefono,
            peso = peso,
            altura = altura,
            genero = genero,
            grupoSanguineo = grupoSanguineo,
            direccion = direccion,
            )


        RegistroDonacion.objects.create(donante=donante_obj)

        return donante_obj

class UsuarioLoginSerializer(ModelSerializer):
    # token = CharField(allow_blank=True, read_only=True)
    username = CharField(allow_blank=True, required=False)
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            # 'token',
        ]

    def validate(self, data):
        user_obj = None
        username = data["username"]
        password = data["password"]
        user = User.objects.filter(Q(username=username))

        if user.exists():
            user_obj = user.first()
        else:
            raise ValidationError("El usuario no existe.")

        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("La contraseña es incorrecta, intente de nuevo.")
        
            # else:
            #     data["token"] = "TOKEN GENERADO"
        
        return data