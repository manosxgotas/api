from rest_framework_jwt.views import (
    obtain_jwt_token,
    verify_jwt_token,
    )
from django.conf.urls import url

from .views import (
    DonanteRegistroAPI,
    activar_cuenta,
    reset_pass_request,
    reset_pass
    )

urlpatterns = [
    url(r'^registro/$', DonanteRegistroAPI.as_view(), name='registro'),
    url(r'^activar-cuenta-link/(?P<token>[^/]+)$', activar_cuenta , name='activar-cuenta-link'),
    url(r'^activar-cuenta-clave/$', activar_cuenta, name='activar-cuenta-clave'),
    url(r'^reset-pass-request/$', reset_pass_request, name='reset-pass-request'),
    url(r'^reset-pass/', reset_pass, name='reset-pass'),
    url(r'^reset-pass-token/(?P<token>[^/]+)$', reset_pass, name='reset-pass-token'),
    url(r'^token/$', obtain_jwt_token, name='token'),
    url(r'^verificar-token/$', verify_jwt_token, name='verificar-token'),
]