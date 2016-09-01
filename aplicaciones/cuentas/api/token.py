from itsdangerous import (
    URLSafeTimedSerializer,
    TimedSerializer
)
from manosxgotas.settings.local import (
    SECRET_KEY,
    SECURITY_PASSWORD_SALT,
    FRONTEND_URL
)
from django.template import loader
from django.core.mail import EmailMultiAlternatives


def generar_token_confirmacion(key, url=False):
    '''
    Generación de serializer parseado mediante la clave privada
    de la app y obtención del token a partir del email/id firmado
    con la clave de seguridad 'SALT'.
    '''
    if url:
        serializer = URLSafeTimedSerializer(SECRET_KEY)
    else:
        serializer = TimedSerializer(SECRET_KEY)
    return serializer.dumps(key, salt=SECURITY_PASSWORD_SALT)


def confirmar_token(token, url=False, vencimiento=43200):
    '''
    Proceso inverso para obtener email/id a confirmar mediante
    el procesamiento del token.
    '''
    if url:
        serializer = URLSafeTimedSerializer(SECRET_KEY)
    else:
        serializer = TimedSerializer(SECRET_KEY)
    try:
        key = serializer.loads(
            token,
            salt=SECURITY_PASSWORD_SALT,
            max_age=vencimiento
        )
    except:
        return False
    return key


def enviar_mail_activacion(usuario):
    # Se genera token con email del usuario.
    token_link = generar_token_confirmacion(usuario.email, url=True)
    token_clave = generar_token_confirmacion(usuario.id)

    # Creación de URL de confirmación
    confirm_url = FRONTEND_URL + 'activar-cuenta/' + token_link

    # Obtención de templates html y txt de emails.
    htmly = loader.get_template('emails/html/confirmar_cuenta.html')
    text = loader.get_template('emails/txt/confirmar_cuenta.txt')

    # Definición de variables de contexto
    variables = {
        'usuario': usuario,
        'confirm_url': confirm_url,
        'clave': token_clave
    }
    html_content = htmly.render(variables)
    text_content = text.render(variables)

    # Creación y envío de email.
    msg = EmailMultiAlternatives(
        'Bienvenido a Manos por gotas',
        text_content,
        to=[usuario.email]
    )

    msg.attach_alternative(html_content, "text/html")
    msg.send()
