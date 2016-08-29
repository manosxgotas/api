from rest_framework_jwt.views import (
    obtain_jwt_token,
    verify_jwt_token,
    )
from django.conf.urls import url

from .views import (
    DonanteRegistroAPI,
    activar_cuenta
    )

urlpatterns = [
    url(r'^registro/$', DonanteRegistroAPI.as_view() , name='registro'),
    url(r'^activar-cuenta-link/(?P<token>[^/]+)$', activar_cuenta , name='activar-cuenta-link'),
    url(r'^activar-cuenta-clave/$', activar_cuenta , name='activar-cuenta-clave'),
    url(r'^token/$', obtain_jwt_token , name='token'),
    url(r'^verificar-token/$', verify_jwt_token , name='verificar-token'),
]