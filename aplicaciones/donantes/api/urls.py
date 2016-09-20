from django.conf.urls import url

from .views import (
    DonantePerfilAPI,
    DonanteUpdateAPI,
    DonanteUpdateDireccionAPI,
    DonanteUpdateAvatarAPI,
    )

urlpatterns = [

    url(
        r'^perfil/(?P<usuario_id>\w+)$',
        DonantePerfilAPI.as_view(),
        name='perfil'
        ),

    url(
        r'^perfil/edit/(?P<usuario_id>\w+)$',
        DonanteUpdateAPI.as_view(),
        name='perfil_edit'
        ),

    url(
        r'^perfil/edit/direccion/(?P<usuario_id>\w+)$',
        DonanteUpdateDireccionAPI.as_view(),
        name='perfil_edit_direccion'
        ),

    url(
        r'^perfil/edit/avatar/(?P<usuario_id>\w+)$',
        DonanteUpdateAvatarAPI.as_view(),
        name='perfil_edit_avatar'
        ),

]
