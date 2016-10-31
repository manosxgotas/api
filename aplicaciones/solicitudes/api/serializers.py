import datetime
import json
from rest_framework.serializers import (
    ModelSerializer,
    FileField,
    JSONField,
    ListField,
    SerializerMethodField
    )
from rest_framework.validators import ValidationError
from aplicaciones.base.models import (
    SolicitudDonacion,
    TipoSolicitudDonacion,
    Direccion,
    Paciente,
    Localidad,
    GrupoSanguineoSolicitud,
    GrupoSanguineo,
    ImagenSolicitudDonacion
    )
from aplicaciones.base.api.serializers import CentroDonacionSerializer


class DireccionSerializer(ModelSerializer):

    class Meta:
        model = Direccion
        fields = [
            'calle',
            'numero',
            'piso',
            'numeroDepartamento',
            'localidad',
        ]


class ImagenSolicitudDonacionSerializer(ModelSerializer):

    class Meta:
        model = ImagenSolicitudDonacion
        fields = '__all__'


class GrupoSanguineoSerializer(ModelSerializer):
    class Meta:
        model = GrupoSanguineo
        fields = [
            'nombre'
        ]


class GrupoSanguineoSolicitudSerializer(ModelSerializer):
    grupoSanguineo = GrupoSanguineoSerializer()

    class Meta:
        model = GrupoSanguineoSolicitud
        fields = [
            'solicitud',
            'grupoSanguineo',
        ]


class PacienteSerializer(ModelSerializer):
    direccion = DireccionSerializer()
    edad = SerializerMethodField()

    class Meta:
        model = Paciente
        fields = [
            'id',
            'nombre',
            'apellido',
            'email',
            'nacimiento',
            'telefono',
            'genero',
            'direccion',
            'edad'
        ]

    def get_edad(self, obj):
        today = datetime.date.today()
        return today.year - obj.nacimiento.year - ((today.month, today.day) < (obj.nacimiento.month, obj.nacimiento.day))


class SolicitudDonacionListadoSerializer(ModelSerializer):
    gruposSanguineos = GrupoSanguineoSolicitudSerializer(many=True)
    imagenesSolicitud = ImagenSolicitudDonacionSerializer(many=True)
    centroDonacion = CentroDonacionSerializer()
    paciente = PacienteSerializer()

    class Meta:
        model = SolicitudDonacion
        fields = [
            'id',
            'titulo',
            'fechaPublicacion',
            'donantesNecesarios',
            'video',
            'fechaHoraInicio',
            'fechaHoraFin',
            'paciente',
            'tipo',
            'centroDonacion',
            'paciente',
            'donante',
            'gruposSanguineos',
            'imagenesSolicitud'
        ]


def create_solicitud_donacion_serializer(usuario):
    class SolicitudDonacionCreateSerializer(ModelSerializer):
        grupos = ListField(
            required=False,
            write_only=True
            )
        imagenes = ListField(
            child=FileField(),
            required=False,
            write_only=True
            )
        paciente = JSONField(binary=True, write_only=True)

        class Meta:
            model = SolicitudDonacion
            fields = [
                'titulo',
                'donantesNecesarios',
                'video',
                'fechaHoraInicio',
                'fechaHoraFin',
                'tipo',
                'centroDonacion',
                'paciente',
                'grupos',
                'imagenes',
                'historia'
            ]

        def validate(self, data):
            datetime_now = datetime.datetime.now()
            if data['fechaHoraInicio'] < datetime_now:
                raise ValidationError('La fecha de inicio no puede ser menor a la fecha actual')
            else:
                if data['fechaHoraFin'] < data['fechaHoraInicio']:
                    raise ValidationError('La hora de finalizacion no puede ser menor a la hora de inicio')
            return data

        def create(self, validated_data):

            # Obtengo los datos ingresados.
            titulo = validated_data['titulo']
            donantesNecesarios = validated_data['donantesNecesarios']
            video = validated_data.get('video', None)
            fechaHoraInicio = validated_data.get('fechaHoraInicio')
            fechaHoraFin = validated_data.get('fechaHoraFin')
            tipo = validated_data['tipo']
            centroDonacion = validated_data['centroDonacion']
            historia = validated_data.get('historia', None)
            imagenes = validated_data.get('imagenes', None)
            paciente_data = validated_data.pop('paciente')
            direccion_data = paciente_data.pop('direccion')

            localidad_id = direccion_data.pop('localidad')
            localidad = Localidad.objects.get(id=localidad_id)
            direccion_obj = Direccion.objects.create(
                localidad=localidad,
                **direccion_data
            )

            paciente_obj = Paciente.objects.create(
                direccion=direccion_obj,
                **paciente_data
            )

            donante = usuario.donante

            # Creo objeto SolicitudDonacion
            solicitudDonacion = SolicitudDonacion.objects.create(
                titulo=titulo,
                donantesNecesarios=donantesNecesarios,
                video=video,
                fechaHoraInicio=fechaHoraInicio,
                fechaHoraFin=fechaHoraFin,
                tipo=tipo,
                centroDonacion=centroDonacion,
                historia=historia,
                paciente=paciente_obj,
                donante=donante
            )

            # Obtengo los grupos sanguineos necesarios para la donacion
            grupos = validated_data.pop('grupos')

            # Le asocio cada grupo sanguineo a la solicitud
            for val in grupos:
                # Convierto de json a list
                val = json.loads(val)
                # for each sobre la lista
                for valor in val:
                    if (int(valor)):
                        grupoSanguineo = GrupoSanguineo.objects.get(id=valor)
                        GrupoSanguineoSolicitud.objects.create(
                            solicitud=solicitudDonacion,
                            grupoSanguineo=grupoSanguineo
                        )

            if imagenes is not None:
                for index, imagen in enumerate(imagenes):
                    if index == 0:
                        ImagenSolicitudDonacion.objects.create(
                            imagen=imagen,
                            portada=True,
                            solicitud=solicitudDonacion
                        )
                    else:
                        ImagenSolicitudDonacion.objects.create(
                            imagen=imagen,
                            solicitud=solicitudDonacion
                        )

            return solicitudDonacion
    return SolicitudDonacionCreateSerializer


class SolicitudDonacionInfoSerializer(ModelSerializer):
    centroDonacion = CentroDonacionSerializer()
    paciente = PacienteSerializer()
    gruposSanguineos = GrupoSanguineoSolicitudSerializer(many=True)
    imagenesSolicitud = ImagenSolicitudDonacionSerializer(many=True)

    class Meta:
        model = SolicitudDonacion
        fields = [
            'titulo',
            'fechaPublicacion',
            'donantesNecesarios',
            'video',
            'fechaHoraInicio',
            'fechaHoraFin',
            'tipo',
            'centroDonacion',
            'paciente',
            'donante',
            'gruposSanguineos',
            'imagenesSolicitud',
            'historia'
        ]


class TipoSolicitudSerializer(ModelSerializer):

    class Meta:
        model = TipoSolicitudDonacion
        fields = '__all__'
