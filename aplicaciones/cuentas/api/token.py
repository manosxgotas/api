from itsdangerous import URLSafeTimedSerializer
from manosxgotas.settings.local import (
    SECRET_KEY,
    SECURITY_PASSWORD_SALT
    )


def generar_token_confirmacion(email):
    '''
    Generación de serializer parseado mediante la clave privada
    de la app y se obtiene el token a partir del email y firmado
    con la clave privada 'SALT'.
    '''
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    return serializer.dumps(email, salt=SECURITY_PASSWORD_SALT)

def confirmar_token(token, vencimiento=10800):
    '''
    Proceso inverso para obtener email a confirmar mediante
    el procesamiento del token.
    '''
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    try:
        email = serializer.loads(
            token,
            salt=SECURITY_PASSWORD_SALT,
            max_age=vencimiento
            )
    except:
        return False
    return email
