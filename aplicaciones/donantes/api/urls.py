from django.conf.urls import url

from .views import (
    DonantePerfilAPI,
    DonanteUpdateAPI,
    )

urlpatterns = [
    
    url(r'^perfil/(?P<usuario_id>\w+)$', DonantePerfilAPI.as_view() , name='perfil'),
    url(r'^perfil/edit/(?P<usuario_id>\w+)$', DonanteUpdateAPI.as_view() , name='perfil_edit'),

]