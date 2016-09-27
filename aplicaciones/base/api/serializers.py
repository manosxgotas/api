from rest_framework import serializers
from rest_framework.serializers import (
    ModelSerializer,
    )
from aplicaciones.base.models import (
    CentroDonacion,
    Donante,
    Evento,
    GrupoSanguineo,
    HorarioCentroDonacion,
    Nacionalidad,
    ImagenEvento,
    LugarEvento,
    TipoDocumento
    )


class GrupoSanguineoSerializer(ModelSerializer):

    class Meta:
        model = GrupoSanguineo
        fields = '__all__'


class NacionalidadSerializer(ModelSerializer):

    class Meta:
        model = Nacionalidad
        fields = '__all__'


class TipoDocumentoSerializer(ModelSerializer):

    class Meta:
        model = TipoDocumento
        fields = '__all__'


class DonanteSerializer(ModelSerializer):
    class Meta:
        model = Donante
        fields = '__all__'


class HorarioCentroDonacionSerializer(ModelSerializer):
    class Meta:
        model = HorarioCentroDonacion
        fields = '__all__'


class CentroDonacionSerializer(ModelSerializer):
    horarios = HorarioCentroDonacionSerializer(many=True)

    class Meta:
        model = CentroDonacion
        fields = [
            'id',
            'nombre',
            'tipo',
            'telefono',
            'lugarDonacion',
            'horarios'
        ]
        depth = 4


class LugarEventoSerializer(ModelSerializer):
    class Meta:
        model = LugarEvento
        fields = '__all__'
        depth = 4


class ImagenEventoSerializer(ModelSerializer):
    class Meta:
        model = ImagenEvento
        fields = '__all__'


class EventoSerializer(ModelSerializer):
    imagenesEvento = ImagenEventoSerializer(many=True)
    lugarEvento = LugarEventoSerializer(many=True)

    class Meta:
        model = Evento
        fields = [
            'id',
            'nombre',
            'fechaHoraInicio',
            'fechaHoraFin',
            'categoria',
            'descripcion',
            'imagenesEvento',
            'lugarEvento',
            'video'
        ]
        depth = 1


class GrupoSanguineoInfoSerializer(ModelSerializer):
    class Meta:
        model = GrupoSanguineo
        fields = '__all__'
        depth = 1
