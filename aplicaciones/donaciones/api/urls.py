from django.conf.urls import url

from .views import (
    DonacionAltaAPI,
    )


urlpatterns = [
    url(r'^crear/$', DonacionAltaAPI.as_view() , name='alta-donacion'),
]