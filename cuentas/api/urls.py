from rest_framework_jwt.views import (
	obtain_jwt_token,
	verify_jwt_token,
	)
from django.conf.urls import url

from .views import (
	DonanteRegistroAPI, 
	UsuarioLoginAPI,
	)

urlpatterns = [

    url(r'^registro/$', DonanteRegistroAPI.as_view() , name='registro'),
    url(r'^login/$', UsuarioLoginAPI.as_view() , name='login'),
    url(r'^token/$', obtain_jwt_token , name='token'),
    url(r'^verificar-token/$', verify_jwt_token , name='verificar-token'),
]