from rest_framework.generics import CreateAPIView

from rest_framework.permissions import AllowAny

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from django.contrib.auth import get_user_model


from aplicaciones.base.models import (
    Donante,
    )

from .serializers import (
    DonanteRegistroSerializer,
    )

class DonanteRegistroAPI(CreateAPIView):

    permission_classes = [AllowAny]
    queryset = Donante.objects.all()
    serializer_class = DonanteRegistroSerializer