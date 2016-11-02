from rest_framework.generics import (
    RetrieveAPIView,
    UpdateAPIView,
    )

from rest_framework.parsers import FormParser, MultiPartParser

from aplicaciones.base.models import (
    Donante
    )

from .serializers import (
    DonantePerfilSerializer,
    DonanteUpdateSerializer,
    DonanteUpdateDireccionSerializer,
    DonanteUpdateAvatarSerializer,
    )


class DonantePerfilAPI(RetrieveAPIView):
    serializer_class = DonantePerfilSerializer
    queryset = Donante.objects.all()

    def get_object(self):
        return self.request.user.donante


class DonanteUpdateAPI(UpdateAPIView):
    serializer_class = DonanteUpdateSerializer
    queryset = Donante.objects.all()

    def get_object(self):
        return self.request.user.donante


class DonanteUpdateDireccionAPI(UpdateAPIView):
    serializer_class = DonanteUpdateDireccionSerializer
    queryset = Donante.objects.all()

    def get_object(self):
        return self.request.user.donante


class DonanteUpdateAvatarAPI(UpdateAPIView):
    parser_classes = [FormParser, MultiPartParser]
    serializer_class = DonanteUpdateAvatarSerializer
    queryset = Donante.objects.all()

    def get_object(self):
        return self.request.user.donante
