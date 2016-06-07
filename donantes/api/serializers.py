from rest_framework.serializers import (
    ModelSerializer,
    EmailField,
    ValidationError,
    CharField,
    ModelField,
    )
from app.models import (
    Donante, 
    RegistroDonacion,
    Direccion,
    Localidad,
    GrupoSanguineo,
    )

from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class UsuarioPerfilSerializer(ModelSerializer):
     class Meta:
        model = User
        fields = [
        'username',
        'email',
        'first_name',
        'last_name',
        ]

class DireccionPerfilSerializer(ModelSerializer):
    class Meta:
        model = Direccion
        fields = [
        'calle',
        'numero',
        'piso',
        'numeroDepartamento',
        'localidad'
        ]

class GrupoSanguineoPerfilSerializer(ModelSerializer):
    class Meta:
        model = GrupoSanguineo
        fields = [
        'id',
        'nombre'
        ]

class DonantePerfilSerializer(ModelSerializer):
    usuario = UsuarioPerfilSerializer()
    direccion = DireccionPerfilSerializer()
    grupoSanguineo = GrupoSanguineoPerfilSerializer()
    class Meta:
        model = Donante
        fields = [
        'usuario',
        'foto',
        'nacimiento',
        'telefono',
        'peso',
        'altura',
        'genero',
        'grupoSanguineo',
        'direccion',
        ]

class UsuarioUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
        'first_name',
        'last_name',
        ]


class DireccionUpdateSerializer(ModelSerializer):
    class Meta:
        model = Direccion
        fields = [
        'calle',
        'numero',
        'piso',
        'numeroDepartamento',
        'localidad',
        ]

class DonanteUpdateSerializer(ModelSerializer):
    usuario = UsuarioUpdateSerializer()
    direccion = DireccionUpdateSerializer()
    class Meta:
        model = Donante
        fields = [
        'usuario',
        'nacimiento',
        'telefono',
        'peso',
        'altura',
        'grupoSanguineo',
        'direccion',
        ]