from rest_framework.serializers import (
    ModelSerializer,
    IntegerField,
    SerializerMethodField
    )
from aplicaciones.base.models import (
    Donante,
    Direccion,
    Localidad,
    GrupoSanguineo,
    )

from django.contrib.auth import get_user_model

User = get_user_model()


class UsuarioPerfilSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
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
    cantidad_donaciones = SerializerMethodField()
    cantidad_donaciones_pendientes = SerializerMethodField()
    cantidad_donaciones_verificadas = SerializerMethodField()

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
            'cantidad_donaciones',
            'cantidad_donaciones_pendientes',
            'cantidad_donaciones_verificadas'
        ]

    def get_cantidad_donaciones(self, obj):
        return obj.registro.donaciones.count()

    def get_cantidad_donaciones_pendientes(self, obj):
        cantidad = 0
        donaciones = obj.registro.donaciones.all()
        if donaciones.exists():
            for donacion in donaciones:
                ultimo_estado = donacion.historicoEstados.last().estado.nombre
                if ultimo_estado == "Pendiente":
                    cantidad += 1

        return cantidad

    def get_cantidad_donaciones_verificadas(self, obj):
        cantidad = 0
        donaciones = obj.registro.donaciones.all()
        if donaciones.exists():
            for donacion in donaciones:
                ultimo_estado = donacion.historicoEstados.last().estado.nombre
                if ultimo_estado == "Verificada":
                    cantidad += 1

        return cantidad


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

        return instance


class DonanteUpdateDireccionSerializer(ModelSerializer):
    direccion = DireccionUpdateSerializer()

    class Meta:
        model = Donante
        fields = ['direccion']

    def update(self, instance, validated_data):
        direccion_data = validated_data.pop('direccion')
        localidad_data = direccion_data.pop('localidad')
        if instance.direccion is not None:
            direccion = instance.direccion

            direccion.calle = direccion_data.get('calle', direccion.calle)
            direccion.numero = direccion_data.get('numero', direccion.numero)
            direccion.piso = direccion_data.get('piso', direccion.piso)
            direccion.numeroDepartamento = direccion_data.get('numeroDepartamento', direccion.numeroDepartamento)

            localidad_obj = Localidad.objects.filter(id=localidad_data.get('id'))
            if localidad_obj.exists():
                direccion.localidad = localidad_obj.first()
            direccion.save()

        else:
            instance.direccion = Direccion.objects.create(
                    calle=direccion_data['calle'],
                    numero=direccion_data['numero'],
                    piso=direccion_data.get('piso', None),
                    numeroDepartamento=direccion_data.get('numeroDepartamento', None),
                    localidad=Localidad.objects.get(id=localidad_data['id'])
                )

        instance.save()
        return instance


class DonanteUpdateAvatarSerializer(ModelSerializer):
    class Meta:
        model = Donante
        fields = ['foto']

    def update(self, instance, validated_data):
        foto_nueva = validated_data.get('foto')
        if instance.foto:
            instance.foto.delete()
        instance.foto = foto_nueva
        instance.save()

        return instance
