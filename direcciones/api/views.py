from .serializers import (
	ProvinciaSerializer,
	LocalidadSerializer
	)

from app.models import Provincia, Localidad

from rest_framework.generics import ListAPIView

from rest_framework.permissions import AllowAny


class ProvinciaListAPI(ListAPIView):
    
    permission_classes = [AllowAny]
    queryset = Provincia.objects.all()
    serializer_class = ProvinciaSerializer

class LocalidadListAPI(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = LocalidadSerializer

    def get_queryset(self):
    	queryset = Localidad.objects.all()
    	provincia_id = self.kwargs['provincia_id']
    	return Localidad.objects.filter(provincia__id=provincia_id)