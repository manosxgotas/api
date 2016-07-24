import datetime

from rest_framework.serializers import (
    ModelSerializer,
    )

from rest_framework.validators import ValidationError

from aplicaciones.base.models import (
    RegistroDonacion,
    Donacion,
    EstadoDonacion,
    HistoricoEstadoDonacion
    )

class DonacionCreateSerializer(ModelSerializer):
    class Meta:
        model = Donacion
        fields = '__all__'

    def validate_fechaHora(self, value):
        if value > datetime.datetime.now():
            raise ValidationError('La fecha y hora ingresada no pueden ser futuras.')
        return value

    def create(self, validated_data):
        donacion = Donacion(**validated_data)
        donacion.save()

        estado = EstadoDonacion.objects.get(nombre='Pendiente')

        historico = HistoricoEstadoDonacion(
            inicio = datetime.datetime.now(),
            estado = estado,
            donacion = donacion
            )
        historico.save()

        return donacion

class DonacionUpdateSerializer(ModelSerializer):
    class Meta:
        model = Donacion
        fields = [
        'fechaHora',
        'foto',
        'descripcion',
        'evento',
        'lugarDonacion'
        ]

    def update(self, instance, validated_data):
        instance.fechaHora = validated_data.get('fechaHora', instance.fechaHora)
        instance.lugarDonacion = validated_data.get('lugarDonacion', instance.lugarDonacion)
        instance.evento = validated_data.get('evento', instance.evento)
        instance.descripcion = validated_data.get('descripcion', instance.descripcion)
        foto_nueva = validated_data.get('foto', None)

        if foto_nueva is not None:
            if instance.foto:
                instance.foto.delete()
            instance.foto = foto_nueva

        instance.save()
        return instance

class DonacionPerfilSerializer(ModelSerializer):
    class Meta:
        model = Donacion
        depth = 2
        fields = [
        'id',
        'fechaHora',
        'registro',
        'foto',
        'evento',
        'verificacion',
        'lugarDonacion',
        'historicoEstados'
        ]

class RegistroDonacionSerializer(ModelSerializer):
    donaciones = DonacionPerfilSerializer(many=True)
    depth = 1
    class Meta:
        model = RegistroDonacion
        fields = [
        'id',
        'privado',
        'donaciones'
        ]