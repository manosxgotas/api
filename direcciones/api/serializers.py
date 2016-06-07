from rest_framework.serializers import (
    ModelSerializer,
    )

from app.models import (
    Provincia,
    Localidad
    )

class LocalidadSerializer(ModelSerializer):

    class Meta:
        model = Localidad
        fields = [
        'id',
        'nombre',
        ]

class ProvinciaSerializer(ModelSerializer):
    class Meta:
        model = Provincia
        fields = [
        'id',
        'nombre',
        ]


