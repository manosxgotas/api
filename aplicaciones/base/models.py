import os, datetime

from manosxgotas.settings.local import MEDIA_ROOT

from django.utils.crypto import get_random_string
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

DIAS_SEMANA = {
    '1': _(u'Lunes'),
    '2': _(u'Martes'),
    '3': _(u'Miércoles'),
    '4': _(u'Jueves'),
    '5': _(u'Viernes'),
    '6': _(u'Sábado'),
    '7': _(u'Domingo'),
}

GENEROS = {
    '1': _(u'Hombre'),
    '2': _(u'Mujer'),
}

DIAS_DONACION_POR_GENERO = {
    '1': 60,
    '2': 90,
}


def validate_fecha_hora_futuro(value):
    if value > datetime.datetime.now():
        raise ValidationError('La fecha y hora ingresada no pueden ser futuras.')


def establecer_destino_imagen_ubicacion(instance, imagename):
    # Almacena la imágen en: 'media/donantes/fotos/<nombre usuario>.<extension>'
    # si es donante.
    if (isinstance(instance, Donante)):
        ruta_imagenes_ubicacion = 'donantes/fotos/'
    # Almacena la imágen en: 'media/donaciones/<nombre usuario>/<str donacion>.<extension>'
    # si es una donación.
    if (isinstance(instance, Donacion)):
        owner = str(instance.registro.donante)
        ruta_imagenes_ubicacion = 'donaciones/' + owner + '/'
    # Almacena la imágen en:
    # 'media/donaciones/<nombre usuario>/verificaciones/<str donacion>/<str verificacion>.<extension>'
    # si es una verificación.
    if (isinstance(instance, VerificacionDonacion)):
        owner = str(instance.donacion.registro.donante)
        donacion = str(instance.donacion)
        ruta_imagenes_ubicacion = 'donaciones/' + owner + '/verificaciones/' + donacion + '/'
    extension_imagen = imagename.split('.')[-1] if '.' in imagename else ''
    nombre_imagen = '%s.%s' % (slugify(str(instance)), extension_imagen)
    return os.path.join(ruta_imagenes_ubicacion, nombre_imagen)


class GenerosField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = tuple(sorted(GENEROS.items()))
        kwargs['max_length'] = 1
        super(GenerosField, self).__init__(*args, **kwargs)


class DiasSemanaField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = tuple(sorted(DIAS_SEMANA.items()))
        kwargs['max_length'] = 1
        super(DiasSemanaField, self).__init__(*args, **kwargs)


class Donante(models.Model):
    usuario = models.ForeignKey(User)
    numeroDocumento = models.PositiveIntegerField(unique=True, verbose_name='número de documento')
    tipoDocumento = models.ForeignKey('TipoDocumento', verbose_name='tipo de documento')
    foto = models.ImageField(null=True, blank=True, upload_to=establecer_destino_imagen_ubicacion)
    telefono = models.CharField(max_length=20, verbose_name='teléfono')
    nacimiento = models.DateField(verbose_name='fecha de nacimiento')
    peso = models.DecimalField(max_digits=4, decimal_places=1)
    altura = models.PositiveIntegerField(validators=[MinValueValidator(100), MaxValueValidator(350)])
    genero = GenerosField(verbose_name='género')
    grupoSanguineo = models.ForeignKey('GrupoSanguineo', null=True, verbose_name='grupo sanguíneo')
    direccion = models.ForeignKey('Direccion', verbose_name='dirección')
    nacionalidad = models.ForeignKey('Nacionalidad')

    def get_genero(self):
        return GENEROS.get(self.genero)

    def __str__(self):
        return self.usuario.username


class Nacionalidad(models.Model):
    nombre = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'nacionalidades'


class TipoDocumento(models.Model):
    siglas = models.CharField(max_length=20)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.siglas

    class Meta:
        verbose_name = 'tipo de documento'
        verbose_name_plural = 'tipos de documento'


class Direccion(models.Model):
    calle = models.CharField(max_length=50)
    numero = models.PositiveSmallIntegerField(verbose_name='número')
    piso = models.SmallIntegerField(blank=True, null=True)
    numeroDepartamento = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='número de departamento')
    localidad = models.ForeignKey('Localidad')

    def __str__(self):
        return self.calle + '-' + str(self.numero)

    class Meta:
        verbose_name = 'dirección'
        verbose_name_plural = 'direcciones'


class Localidad(models.Model):
    nombre = models.CharField(max_length=50)
    provincia = models.ForeignKey('Provincia')

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'localidad'
        verbose_name_plural = 'localidades'


class Provincia(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class GrupoSanguineo(models.Model):
    nombre = models.CharField(max_length=5)
    puedeDonarA = models.ManyToManyField('self', blank=True, verbose_name='puede donar a')

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'grupo sanguíneo'
        verbose_name_plural = 'grupos sanguíneos'


class RegistroDonacion(models.Model):
    privado = models.BooleanField(default=True)
    donante = models.OneToOneField('Donante', related_name='registro')

    def __str__(self):
        return 'Registro de donación de ' + self.donante.usuario.username

    class Meta:
        verbose_name = 'registro de donación'
        verbose_name_plural = 'registros de donación'


class Donacion(models.Model):
    fechaHora = models.DateTimeField(verbose_name='fecha y hora', validators=[validate_fecha_hora_futuro])
    foto = models.ImageField(blank=True, upload_to=establecer_destino_imagen_ubicacion)
    descripcion = models.TextField(blank=True, verbose_name='descripción')
    registro = models.ForeignKey('RegistroDonacion', related_name='donaciones', verbose_name='registro de donación')
    verificacion = models.OneToOneField('VerificacionDonacion', blank=True, null=True, verbose_name='verificación', related_name='donacion')
    lugarDonacion = models.ForeignKey('LugarDonacion', verbose_name='lugar de donación')

    def __str__(self):
        return 'Donación de ' + str(self.registro.donante) + ' - ' + str(self.fechaHora)

    class Meta:
        verbose_name = 'donación'
        verbose_name_plural = 'donaciones'


class EstadoDonacion(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'estado de la donación'
        verbose_name_plural = 'estados de la donación'


class HistoricoEstadoDonacion(models.Model):
    inicio = models.DateTimeField()
    fin = models.DateTimeField(null=True, blank=True)
    donacion = models.ForeignKey('Donacion', related_name='historicoEstados')
    estado = models.ForeignKey('EstadoDonacion')

    def __str__(self):
        return 'Histórico ' + str(self.id)

    class Meta:
        verbose_name = 'histórico de estados de donación'
        verbose_name_plural = 'históricos de estados de donación'


class VerificacionDonacion(models.Model):
    imagen = models.ImageField(upload_to=establecer_destino_imagen_ubicacion)

    class Meta:
        verbose_name = 'verificación de donación'
        verbose_name_plural = 'verificaciones de donación'


class SolicitudDonacion(models.Model):
    titulo = models.CharField(max_length=50)
    fechaPublicacion = models.DateField(verbose_name='fecha de publicación')
    donantesNecesarios = models.SmallIntegerField(verbose_name='cantidad de donantes necesarios')
    video = models.FileField()
    fechaHoraInicio = models.DateTimeField(verbose_name='fecha y hora de inicio')
    fechaHoraFin = models.DateTimeField(verbose_name='fecha y hora de fin')
    estado = models.ForeignKey('EstadoSolicitudDonacion', verbose_name='estado de solicitud de donación')
    tipo = models.ForeignKey('TipoSolicitudDonacion', verbose_name='tipo de solicitud de donación')
    centroDonacion = models.ForeignKey('CentroDonacion', null=True, verbose_name='centro de donación')
    paciente = models.ForeignKey('Paciente')

    def __str__(self):
        return self.fechaPublicacion + '-' + self.titulo

    class Meta:
        verbose_name = 'solicitud de donación'
        verbose_name_plural = 'solicitudes de donación'


class EstadoSolicitudDonacion(models.Model):
    nombre = models.CharField(max_length=20)
    descripcion = models.TextField(blank=True, verbose_name='descripción')

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'estado de solicitud de donación'
        verbose_name_plural = 'estados de solicitud de donación'


class TipoSolicitudDonacion(models.Model):
    nombre = models.CharField(max_length=20)
    descripcion = models.TextField(blank=True, verbose_name='descripción')

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'tipo de solicitud de donación'
        verbose_name_plural = 'tipos de solicitud de donación'


class ImagenSolicitudDonacion(models.Model):
    imagen = models.ImageField()
    solicitud = models.ForeignKey('SolicitudDonacion')

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = 'imagen de solicitud de donación'
        verbose_name_plural = 'imágenes de solicitud de donación'


class GrupoSanguineoSolicitud(models.Model):
    solicitud = models.ForeignKey('SolicitudDonacion')
    grupoSanguineo = models.ForeignKey('GrupoSanguineo', verbose_name='grupo sanguíneo')

    def __str__(self):
        return self.id + '-' + self.solicitud.__str__ + '-' + self.grupoSanguineo.nombre

    class Meta:
        verbose_name = 'grupo sanguíneo de la solicitud de donación'
        verbose_name_plural = 'grupos sanguíneos de la solicitud de donación'


class Evento(models.Model):
    nombre = models.CharField(max_length=100)
    fechaHoraInicio = models.DateTimeField(verbose_name='fecha y hora de inicio')
    fechaHoraFin = models.DateTimeField(verbose_name='fecha y hora de finalización')
    descripcion = models.TextField(blank=True, verbose_name='descripción')
    video = models.FileField(blank=True, null=True)
    categoria = models.ForeignKey('CategoriaEvento', verbose_name='categoría del evento')

    def __str__(self):
        return self.nombre


class LugarEvento(models.Model):
    evento = models.ForeignKey('Evento', related_name='lugarEvento')
    lugarDonacion = models.OneToOneField('LugarDonacion', verbose_name='lugar de donación', related_name='lugarEventoDonacion')

    class Meta:
        verbose_name = 'lugar de evento'
        verbose_name_plural = 'lugares de eventos'


class ImagenEvento(models.Model):
    imagen = models.ImageField()
    evento = models.ForeignKey('Evento')

    class Meta:
        verbose_name = 'imagen del evento'
        verbose_name_plural = 'imágenes del evento'


class CategoriaEvento(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True, verbose_name='descripción')

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'categoría del evento'
        verbose_name_plural = 'categorías del evento'


class CentroDonacion(models.Model):
    nombre = models.CharField(max_length=50)
    tipo = models.ForeignKey('TipoCentroDonacion')
    lugarDonacion = models.OneToOneField('LugarDonacion', related_name='lugarCentro', on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'centro de donación'
        verbose_name_plural = 'centros de donación'
        ordering = ['nombre']


class TipoCentroDonacion(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True, verbose_name='descripción')

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'tipo de centro de donación'
        verbose_name_plural = 'tipos de centro de donación'


class HorarioCentroDonacion(models.Model):
    dia = DiasSemanaField()
    horaApertura = models.TimeField(verbose_name='hora de apertura')
    horaCierre = models.TimeField(verbose_name='hora de cierre')

    def get_dia(self):
        return DIAS_SEMANA.get(self.dia)

    class Meta:
        verbose_name = 'horario del centro de donación'
        verbose_name_plural = 'horarios del centro de donación'


class Paciente(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField()
    nacimiento = models.DateField(verbose_name='fecha de nacimiento')
    telefono = models.CharField(max_length=20, verbose_name='teléfono')
    genero = GenerosField()
    direccion = models.ForeignKey('Direccion', verbose_name='dirección')

    def __str__(self):
        return self.nombre + ' ' + self.apellido

    def get_genero(self):
        return GENEROS.get(self.genero)


def obtener_codigo_aleatorio():
    random = get_random_string()
    while CodigoVerificacion.objects.filter(codigo=random).exists():
        random = get_random_string()
    return random


def fecha_vencimiento_defecto():
    return datetime.date.today() + datetime.timedelta(days=30)


class CodigoVerificacion(models.Model):
    codigo = models.CharField(max_length=12, unique=True, default=obtener_codigo_aleatorio)
    fechaEmision = models.DateField(default=datetime.datetime.now, verbose_name='fecha de emisión')
    fechaVencimiento = models.DateField(default=fecha_vencimiento_defecto, verbose_name='fecha de vencimiento')

    def __str__(self):
        return self.codigo

    class Meta:
        verbose_name = 'código de verificación'
        verbose_name_plural = 'códigos de verificación'


class LugarDonacion(models.Model):
    direccion = models.ForeignKey('Direccion', verbose_name='dirección')

    def __str__(self):
        return self.direccion.calle + '_' + str(self.direccion.numero)

    class Meta:
        verbose_name = 'lugar de donación'
        verbose_name_plural = 'lugares de donación'
