from rest_framework_jwt.views import (
    verify_jwt_token,
    )
from django.conf.urls import url, include

from .views import (
    FacebookLogin,
    GoogleLogin,
    activar_cuenta,
    reset_pass_request,
    reset_pass
    )

urlpatterns = [
    url(r'^', include('rest_auth.urls')),
    url(r'^registro/', include('rest_auth.registration.urls')),
    url(r'^social/facebook/$', FacebookLogin.as_view(), name='fb_login'),
    url(r'^social/google/$', GoogleLogin.as_view(), name='google_login'),
    url(r'^activar-cuenta-clave/$', activar_cuenta, name='activar-cuenta-clave'),
    url(r'^reset-pass-request/$', reset_pass_request, name='reset-pass-request'),
    url(r'^reset-pass/', reset_pass, name='reset-pass'),
    url(r'^reset-pass-token/(?P<token>[^/]+)$', reset_pass, name='reset-pass-token'),
    url(r'^verificar-token/$', verify_jwt_token, name='verificar-token'),
]
