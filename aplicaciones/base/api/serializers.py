from rest_framework.serializers import (
    ModelSerializer,
    )
from aplicaciones.base.models import (
    CentroDonacion,
    Donante,
    Evento,
    GrupoSanguineo,
    Nacionalidad,
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

class CentroDonacionSerializer(ModelSerializer):

    class Meta:
        model = CentroDonacion
        fields = '__all__'

class EventoSerializer(ModelSerializer):

    class Meta:
        model = Evento
        fields = '__all__'
