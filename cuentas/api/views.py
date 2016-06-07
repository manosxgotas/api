from rest_framework.generics import CreateAPIView

from rest_framework.permissions import AllowAny

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from django.contrib.auth import get_user_model


from app.models import (
    Donante,
    )

from .serializers import (
    DonanteRegistroSerializer,
    UsuarioLoginSerializer,
    )

class DonanteRegistroAPI(CreateAPIView):

    permission_classes = [AllowAny]
    queryset = Donante.objects.all()
    serializer_class = DonanteRegistroSerializer

class UsuarioLoginAPI(APIView):

    permission_classes = [AllowAny]
    serializer_class = UsuarioLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UsuarioLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)