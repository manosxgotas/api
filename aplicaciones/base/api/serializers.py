from rest_framework.serializers import (
    ModelSerializer,
    )
from aplicaciones.base.models import (
    Donante,
    GrupoSanguineo,
    Nacionalidad,
    TipoDocumento,
    )

from django.contrib.auth import get_user_model
from django.db.models import Q


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