from django.shortcuts import render

from .serializers import (
    DonanteSerializer,
    GrupoSanguineoSerializer,
    NacionalidadSerializer,
    TipoDocumentoSerializer
    )

from aplicaciones.base.models import (
    Donante,
    GrupoSanguineo,
    Nacionalidad,
    TipoDocumento
    )

from rest_framework.generics import ListAPIView, CreateAPIView

from rest_framework.permissions import AllowAny

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from django.contrib.auth import get_user_model

class DonanteListAPI(ListAPIView):
    queryset = Donante.objects.all()
    serializer_class = DonanteSerializer

class GrupoSanguineoListAPI(ListAPIView):
    permission_classes = [AllowAny]
    queryset = GrupoSanguineo.objects.all()
    serializer_class = GrupoSanguineoSerializer

class NacionalidadListAPI(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Nacionalidad.objects.all()
    serializer_class = NacionalidadSerializer

class TipoDocumentoListAPI(ListAPIView):
    permission_classes = [AllowAny]
    queryset = TipoDocumento.objects.all()
    serializer_class = TipoDocumentoSerializer