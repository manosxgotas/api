import os
import dj_database_url

from .local import *

DEBUG = False
TEMPLATE_DEBUG = False

# Configuración de la base de datos en entorno local
DATABASES = {
    'default': dj_database_url.config()
    }