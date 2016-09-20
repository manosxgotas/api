from allauth.account import app_settings as allauth_settings
from allauth.utils import email_address_exists
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email

from rest_framework.serializers import (
    Serializer,
    EmailField,
    CharField,
    ValidationError
)


class RegistroSerializer(Serializer):
    email = EmailField(required=allauth_settings.EMAIL_REQUIRED)
    email2 = EmailField(required=allauth_settings.EMAIL_REQUIRED)
    first_name = CharField(required=True, write_only=True)
    last_name = CharField(required=True, write_only=True)
    password1 = CharField(required=True, write_only=True)
    genero = CharField(required=True, write_only=True, max_length=1)

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise ValidationError(
                    ("Un usuario ya ha sido registrado con este correo electrónico."))
        return email

    def validate_password1(self, password1):
        return get_adapter().clean_password(password1)

    def validate(self, data):
        if data['email'] != data['email2']:
            raise ValidationError(
                ("Los correos electrónicos no coinciden."))
        return data

    def get_cleaned_data(self):
        return {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'genero': self.validated_data.get('genero', '')
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        user.donante.genero = self.cleaned_data['genero']
        user.save()
        return user
