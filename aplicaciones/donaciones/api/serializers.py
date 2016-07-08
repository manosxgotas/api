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

class DonacionSerializer(ModelSerializer):
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
        'centroDonacion',
        'historicoEstados'
        ]

class DonacionAltaSerializer(ModelSerializer):
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

class RegistroDonacionSerializer(ModelSerializer):
    donaciones = DonacionSerializer(many=True)
    depth = 1
    class Meta:
        model = RegistroDonacion
        fields = [
        'id',
        'privado',
        'donaciones'
        ]