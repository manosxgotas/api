from rest_framework.serializers import (
    ModelSerializer,
    EmailField,
    ValidationError,
    CharField,
    ModelField,
    )
from aplicaciones.base.models import (
    Donante,
    GrupoSanguineo,
    Direccion,
    RegistroDonacion,
    )

from django.contrib.auth import get_user_model
from django.db.models import Q


class GrupoSanguineoSerializer(ModelSerializer):

    class Meta:
        model = GrupoSanguineo
        fields = '__all__'

class DonanteSerializer(ModelSerializer):

    class Meta:
        model = Donante
        fields = '__all__'