import os
import dj_database_url

from .local import *

DEBUG = True
TEMPLATE_DEBUG = True

# Configuración de la base de datos en entorno local
DATABASES = {
    'default': dj_database_url.config()
    }