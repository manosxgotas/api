from django.conf.urls import url

from .views import (
    DonantePerfilAPI,
    DonanteUpdateAPI,
    DonanteUpdateDireccionAPI,
    DonanteUpdateAvatarAPI
    )

urlpatterns = [

    url(
        r'^mi-perfil/$',
        DonantePerfilAPI.as_view(),
        name='perfil'
        ),

    url(
        r'^perfil/edit/$',
        DonanteUpdateAPI.as_view(),
        name='perfil_edit'
        ),

    url(
        r'^perfil/edit/direccion/$',
        DonanteUpdateDireccionAPI.as_view(),
        name='perfil_edit_direccion'
        ),

    url(
        r'^perfil/edit/avatar/$',
        DonanteUpdateAvatarAPI.as_view(),
        name='perfil_edit_avatar'
        )

]
