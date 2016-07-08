from rest_framework.serializers import (
    ModelSerializer,
    ValidationError,
    IntegerField
    )
from aplicaciones.base.models import (
    Donante,
    Direccion,
    Localidad,
    GrupoSanguineo,
    )

from aplicaciones.donaciones.api.serializers import (
    RegistroDonacionSerializer
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

class LocalidadPerfilSerializer(ModelSerializer):
     class Meta:
        model = Localidad
        fields = '__all__'

class DireccionPerfilSerializer(ModelSerializer):
    localidad = LocalidadPerfilSerializer()
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
    registro = RegistroDonacionSerializer()
    class Meta:
        model = Donante
        fields = [
        'usuario',
        'numeroDocumento',
        'tipoDocumento',
        'foto',
        'nacimiento',
        'telefono',
        'peso',
        'altura',
        'genero',
        'grupoSanguineo',
        'direccion',
        'nacionalidad',
        'registro'
        ]

class UsuarioUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
        'first_name',
        'last_name',
        ]

class LocalidadUpdateSerializer(ModelSerializer):
     id = IntegerField()
     class Meta:
        model = Localidad
        fields = [
        'id',
        'nombre',
        'provincia'
        ]

class DireccionUpdateSerializer(ModelSerializer):
    localidad = LocalidadUpdateSerializer()
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

    def update(self, instance, validated_data):
        instance.numeroDocumento = validated_data.get('numeroDocumento', instance.numeroDocumento)
        instance.tipoDocumento = validated_data.get('tipoDocumento', instance.tipoDocumento)
        instance.nacimiento = validated_data.get('nacimiento', instance.nacimiento)
        instance.telefono = validated_data.get('telefono', instance.telefono)
        instance.peso = validated_data.get('peso', instance.peso)
        instance.altura = validated_data.get('altura', instance.altura)
        instance.genero = validated_data.get('genero', instance.genero)
        instance.grupoSanguineo = validated_data.get('grupoSanguineo', instance.grupoSanguineo)
        instance.nacionalidad = validated_data.get('nacionalidad', instance.nacionalidad)

        instance.save()

        usuario_data = validated_data.pop('usuario')
        usuario = instance.usuario

        usuario.first_name = usuario_data.get('first_name', usuario.first_name)
        usuario.last_name = usuario_data.get('last_name', usuario.last_name)

        usuario.save()

        direccion_data = validated_data.pop('direccion')
        direccion = instance.direccion

        direccion.calle = direccion_data.get('calle', direccion.calle)
        direccion.numero = direccion_data.get('numero', direccion.numero)
        direccion.piso = direccion_data.get('piso', direccion.piso)
        direccion.numeroDepartamento = direccion_data.get('numeroDepartamento', direccion.numeroDepartamento)

        localidad_data = direccion_data.pop('localidad')

        try:
            localidad_obj = Localidad.objects.get(id=localidad_data.get('id'))
        except:
            localidad_obj = direccion.localidad

        if localidad_obj:
            direccion.localidad = localidad_obj

        direccion.save()

        return instance

class DonanteAvatarSerializer(ModelSerializer):
    class Meta:
        model = Donante
        fields = ['foto']

    def update(self, instance, validated_data):
        instance.foto.delete()
        instance.foto = validated_data['foto']
        instance.save()

        return instance

