from rest_framework.serializers import (
    ModelSerializer,
    )

from aplicaciones.base.models import (
    Localidad,
    LugarDonacion,
    Provincia
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


class LugarDonacionSerializer(ModelSerializer):
    class Meta:
        model = LugarDonacion
        depth = 3
        fields = [
            'id',
            'direccion',
            'lugarEventoDonacion',
            'lugarCentro'
        ]
