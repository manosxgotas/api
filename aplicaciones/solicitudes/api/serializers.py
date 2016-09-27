import datetime
import json
from django.db import transaction
from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    DictField,
    FileField,
    ListField,
    JSONField,
    ImageField,
    IntegerField
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
from aplicaciones.base.api.serializers import CentroDonacionSerializer

def validate_fechaHora(fechaInicio,fechaFin):
    if fechaFin < fechaInicio:
        raise ValidationError('La hora de finalizacion no puede ser menor a la hora de inicio')
    else:
        if fechaInicio < datetime.datetime.now():
            raise ValidationError('La fecha de inicio no puede ser menor a la fecha actual')


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

class SolicitudDonacionListadoSerializer(ModelSerializer):
    gruposSanguineos = GrupoSanguineoSolicitudSerializer(many=True)
    imagenesSolicitud = ImagenSolicitudDonacionSerializer(many=True)
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
            'tipo',
            'centroDonacion',
            'paciente',
            'donante',
            'gruposSanguineos',
            'imagenesSolicitud'
        ]

class SolicitudDonacionCreateSerializer (ModelSerializer):
    grupos = ListField(required=False)
    video = FileField(required=False)
    imagenes = ListField(required=False)
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
            'grupos',
            'imagenes'
        ]
        

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
        grupos = validated_data.pop('grupos')
        #Le asocio cada grupo sanguineo a la solicitud
    
        for val in grupos:
            #Convierto de json a list
            val = json.loads(val)
            # for each sobre la lista
            for valor in val:
                if (int(valor)):
                    grupoSanguineo = GrupoSanguineo.objects.get(id=valor)
                    grupoSanguineoSolicitud = GrupoSanguineoSolicitud.objects.create(
                        solicitud=solicitudDonacion,
                        grupoSanguineo=grupoSanguineo
                    )
                    grupoSanguineoSolicitud.save()
            
            imagenes = validated_data.get('imagenes')
            for value in imagenes:
                print(type(value))
                print(value)
                value = json.loads(value)
                print(type(value))
                print(value)
                for val in value:
                    print(val)
                    imagenSolicitudDonacion = ImagenSolicitudDonacion.objects.create(
                        imagen=val,
                        solicitud=solicitudDonacion
                    )
                    imagenSolicitudDonacion.save()
            

        return solicitudDonacion

class PacienteInfoSerializer(ModelSerializer):
    class Meta:
        model = Paciente
        fields = '__all__'

class SolicitudDonacionInfoSerializer (ModelSerializer):
    centroDonacion = CentroDonacionSerializer()
    paciente = PacienteInfoSerializer()
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
            'imagenesSolicitud'
        ]
        
class TipoSolicitudSerializer(ModelSerializer):

    class Meta:
        model = TipoSolicitudDonacion
        fields = '__all__'

class PacienteCreateSerializer(ModelSerializer):
    direccion = DireccionSerializer()

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
            'direccion'
        ]

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