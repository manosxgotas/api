from .local import *

# Configuración de la base de datos de travis
DATABASES = {
    'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'travis_donacion',
            'USER': 'postgres',
            'HOST': 'localhost'
        }
}