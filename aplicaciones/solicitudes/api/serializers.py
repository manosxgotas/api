import datetime

from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    DictField,
    FileField
    )
from rest_framework.validators import ValidationError
from aplicaciones.base.models import (
    SolicitudDonacion,
    TipoSolicitudDonacion,
    Direccion,
    Paciente,
    GrupoSanguineoSolicitud,
    GrupoSanguineo,
    ImagenSolicitudDonacion
    )


def validate_fechaHora(fechaInicio,fechaFin):
    if fechaFin < fechaInicio:
        raise ValidationError('La hora de finalizacion no puede ser menor a la hora de inicio')
    else:
        if fechaInicio < datetime.datetime.now():
            raise ValidationError('La fecha de inicio no puede ser menor a la fecha actual')


class DireccionPacienteSerializer(ModelSerializer):

    class Meta:
        model = Direccion
        fields = [
            'calle',
            'numero',
            'piso',
            'numeroDepartamento',
            'localidad',
        ]



class SolicitudDonacionCreateSerializer (ModelSerializer):
    gruposSanguineo = DictField(required=False)
    video = FileField(required=False)
    imagenes = DictField(required=False)
    class Meta:
        model = SolicitudDonacion
        fields = '__all__'
        

    def create(self,validated_data):

        #Obtengo los datos ingresados.
        titulo = validated_data['titulo']
        fechaPublicacion = datetime.datetime.now().date()
        donantesNecesarios = validated_data['donantesNecesarios']
        video = validated_data.get('video',None)
        fechaHoraInicio = validated_data.get('fechaHoraInicio')
        fechaHoraFin = validated_data.get('fechaHoraFin')
        tipo = validated_data['tipo']
        centroDonacion = validated_data['centroDonacion']
        paciente = validated_data['paciente']
        donante = validated_data['donante']
        

        
        validate_fechaHora(fechaHoraInicio,fechaHoraFin)
        # Creo objeto SolicitudDonacion

        solicitudDonacion =  SolicitudDonacion.objects.create(
            titulo=titulo,
            fechaPublicacion=fechaPublicacion,
            donantesNecesarios=donantesNecesarios,
            video=video,
            fechaHoraInicio=fechaHoraInicio,
            fechaHoraFin=fechaHoraFin,
            tipo=tipo,
            centroDonacion=centroDonacion,
            paciente=paciente,
            donante=donante
            )

        solicitudDonacion.save()

        #Obtengo los grupos sanguineos necesarios para la donacion
        gruposSanguineo = validated_data.pop('gruposSanguineo')
        #Le asocio cada grupo sanguineo a la solicitud
        for val in gruposSanguineo:
            grupoSanguineo = GrupoSanguineo.objects.get(id=val)
            grupoSanguineoSolicitud = GrupoSanguineoSolicitud.objects.create(
                solicitud=solicitudDonacion,
                grupoSanguineo=grupoSanguineo
                )
            grupoSanguineoSolicitud.save()
            
        imagenes = validated_data.pop('imagenes')

        for value in imagenes:
            imagenSolicitudDonacion = ImagenSolicitudDonacion.objects.create(
                imagen=value,
                solicitud=solicitudDonacion
                )
            imagenSolicitudDonacion.save()

        return solicitudDonacion



class SolicitudDonacionInfoSerializer (ModelSerializer):
    class Meta:
        model = SolicitudDonacion
        fields = '__all__'

class TipoSolicitudSerializer(ModelSerializer):

    class Meta:
        model = TipoSolicitudDonacion
        fields = '__all__'

class PacienteCreateSerializer(ModelSerializer):
    direccion = DireccionPacienteSerializer()

    class Meta:
        model = Paciente
        fields = '__all__'

    def create(self,validated_data):

        #Obtengo los datos ingresados
        nombre = validated_data.get('nombre')
        apellido = validated_data.get('apellido')
        email = validated_data.get('email')
        nacimiento = validated_data.get('nacimiento')
        telefono = validated_data.get('telefono')
        genero = validated_data.get('genero')
        
        
        #Creo objeto Paciente
        paciente = Paciente.objects.create(
            nombre=nombre,
            apellido=apellido,
            email=email,
            nacimiento=nacimiento,
            telefono=telefono,
            genero=genero,
            )

         # Obtención de los datos de la dirección
        direccion_data = validated_data.pop('direccion',None)

        if direccion_data is not None:
             direccion = Direccion(**direccion_data)
             direccion.save()
            
             paciente.direccion = direccion

        paciente.save()

        return paciente