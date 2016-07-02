import datetime

from rest_framework.serializers import (
    ModelSerializer,
    )

from rest_framework.validators import ValidationError

from aplicaciones.base.models import (
    RegistroDonacion,
    DetalleRegistroDonacion,
    )

class DetalleRegistroDonacionSerializer(ModelSerializer):
    class Meta:
        model = DetalleRegistroDonacion
        fields = '__all__'

class RegistroDonacionSerializer(ModelSerializer):
    detalles = DetalleRegistroDonacionSerializer(many=True)
    depth = 1
    class Meta:
        model = RegistroDonacion
        fields = [
        'id',
        'privado',
        'detalles'
        ]