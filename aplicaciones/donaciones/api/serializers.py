import datetime

from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    JSONField
    )

from rest_framework.validators import ValidationError

from aplicaciones.base.models import (
    CentroDonacion,
    Direccion,
    Donacion,
    EstadoDonacion,
    Evento,
    HistoricoEstadoDonacion,
    Localidad,
    LugarDonacion,
    RegistroDonacion
    )

from aplicaciones.direcciones.api.serializers import (
    LugarDonacionSerializer
    )


class DonacionCreateSerializer(ModelSerializer):
    centroDonacion = CharField(write_only=True, required=False)
    evento = CharField(write_only=True, required=False)
    direccion = JSONField(binary=True, write_only=True, required=False)

    class Meta:
        model = Donacion
        fields = [
            'fechaHora',
            'foto',
            'registro',
            'descripcion',
            'centroDonacion',
            'evento',
            'direccion'
        ]

    def validate_fechaHora(self, value):
        if value > datetime.datetime.now():
            raise ValidationError('La fecha y hora ingresada no pueden ser futuras.')
        return value

    def create(self, validated_data):

        # Obtengo datos ingresados.
        fechaHora = validated_data['fechaHora']
        foto = validated_data.get('foto', None)
        registro = validated_data.get('registro')
        descripcion = validated_data.get('descripcion', '')
        lugarDonacion = None

        centroDonacion = validated_data.get('centroDonacion', None)
        evento = validated_data.get('evento', None)
        direccion = validated_data.get('direccion', None)

        # Donación realizada en un centro de donación.
        if centroDonacion is not None:
            centro = CentroDonacion.objects.get(id=centroDonacion)
            lugarDonacion = centro.lugarDonacion
        # Donación realizada en un evento.
        elif evento is not None:
            eventoDonacion = Evento.objects.get(id=evento)
            lugarDonacion = eventoDonacion.lugarEvento.last().lugarDonacion
        # Donación realizada en una dirección en particular.
        elif direccion is not None:
            localidad = Localidad.objects.get(id=int(direccion['localidad']))

            nuevaDireccion = Direccion.objects.create(
                localidad=localidad,
                calle=direccion['calle'],
                numero=direccion['numero']
                )

            lugarDonacion = LugarDonacion.objects.create(
                direccion=nuevaDireccion
                )
        # Si no ingresó ninguna opción de lugar.
        else:
            raise ValidationError('Debes ingresar un lugar donde realizaste tu donación.')

        # Creo objeto donación
        donacion = Donacion.objects.create(
            fechaHora=fechaHora,
            foto=foto,
            registro=registro,
            descripcion=descripcion,
            lugarDonacion=lugarDonacion
            )

        # Seteo estado 'Sin verificar' a la donación.
        estado = EstadoDonacion.objects.get(nombre='Sin verificar')

        historico = HistoricoEstadoDonacion(
            inicio=datetime.datetime.now(),
            estado=estado,
            donacion=donacion
            )

        historico.save()

        return donacion


class DonacionUpdateSerializer(ModelSerializer):
    class Meta:
        model = Donacion
        fields = [
            'fechaHora',
            'foto',
            'descripcion',
            'lugarDonacion'
        ]

    def validate_fechaHora(self, value):
        if value > datetime.datetime.now():
            raise ValidationError('La fecha y hora ingresada no pueden ser futuras.')
        return value

    def update(self, instance, validated_data):
        instance.fechaHora = validated_data.get('fechaHora', instance.fechaHora)
        instance.lugarDonacion = validated_data.get('lugarDonacion', instance.lugarDonacion)
        instance.evento = validated_data.get('evento', instance.evento)
        instance.descripcion = validated_data.get('descripcion', instance.descripcion)
        foto_nueva = validated_data.get('foto', None)

        if foto_nueva is not None:
            if instance.foto:
                instance.foto.delete()
            instance.foto = foto_nueva

        instance.save()
        return instance


class DonacionPerfilSerializer(ModelSerializer):
    lugarDonacion = LugarDonacionSerializer()

    class Meta:
        model = Donacion
        depth = 2
        fields = [
            'id',
            'fechaHora',
            'registro',
            'foto',
            'verificacion',
            'lugarDonacion',
            'historicoEstados',
        ]


class RegistroDonacionSerializer(ModelSerializer):
    donaciones = DonacionPerfilSerializer(many=True)
    depth = 1

    class Meta:
        model = RegistroDonacion
        fields = [
            'id',
            'privado',
            'donaciones'
        ]
