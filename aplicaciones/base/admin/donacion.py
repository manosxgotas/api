# coding=utf-8
import datetime

from django.contrib import admin
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf.urls import url
from django.shortcuts import render
from django.db.models import Count
from chartit import PivotChart, PivotDataPool
from .historicoEstadoDonacion import HistoricoEstadoDonacionInline
from .forms import FormularioEstadisticasDonacion

from ..models import (
    Donacion,
    EstadoDonacion,
    HistoricoEstadoDonacion
)

ESTADO_PENDIENTE = 'pendiente'
ESTADO_VERIFICADA = 'verificada'


def get_estado_donacion(donacion):
    estado_donacion = None
    historicos = donacion.historicoEstados
    if historicos.exists():
        ultimo_historico = historicos.last()
        estado_donacion = ultimo_historico.estado.nombre
    return estado_donacion


def get_lista_fitrada_por_estado(donaciones, estado):
    lista = []
    for donacion in donaciones:
        est = get_estado_donacion(donacion)
        if est == estado:
            lista += donacion
    return lista


class DonacionAdmin(admin.ModelAdmin):
    """
    Especificación de la representación del estado de la solicitud de
     donación en la interfaz de administración.
    """

    def get_urls(self):
        urls = super(DonacionAdmin, self).get_urls()
        add_urls = [
            url(
                r'^verificar/(?P<donacion_id>\d+)$',
                self.admin_site.admin_view(self.verificar),
                name='base_donacion_verificar',
            ),
            url(
                r'^rechazar/(?P<donacion_id>\d+)$',
                self.admin_site.admin_view(self.rechazar),
                name='base_donacion_rechazar',
            ),
            url(
                r'^estadisticas/$',
                self.admin_site.admin_view(self.estadisticas),
                name='base_donacion_estadisticas',
            )
        ]
        return add_urls + urls

    def verificar(self, request, donacion_id):
        donacion_qs = Donacion.objects.filter(id=donacion_id)
        if donacion_qs.exists():
            donacion_obj = donacion_qs.first()
            historicos = donacion_obj.historicoEstados
            if historicos.exists():
                ultimo_historico = historicos.last()
                ultimo_historico.fin = datetime.datetime.now()
                ultimo_historico.save()
                estado_verificada = EstadoDonacion.objects.get(nombre="Verificada")
                HistoricoEstadoDonacion.objects.create(
                    inicio=datetime.datetime.now(),
                    donacion=donacion_obj,
                    estado=estado_verificada,
                )
        return HttpResponseRedirect(
            reverse(
                'admin:base_donacion_changelist'
            )
        )

    def rechazar(self, request, donacion_id):
        donacion_qs = Donacion.objects.filter(id=donacion_id)
        if donacion_qs.exists():
            donacion_obj = donacion_qs.first()
            historicos = donacion_obj.historicoEstados
            if historicos.exists():
                ultimo_historico = historicos.last()
                ultimo_historico.fin = datetime.datetime.now()
                ultimo_historico.save()
                estado_sin_verificar = EstadoDonacion.objects.get(nombre="Sin verificar")
                HistoricoEstadoDonacion.objects.create(
                    inicio=datetime.datetime.now(),
                    donacion=donacion_obj,
                    estado=estado_sin_verificar,
                )
        return HttpResponseRedirect(
            reverse(
                'admin:base_donacion_changelist'
            )
        )

    def estadisticas(self, request):
        context = {
            'site_title': 'Administración de Manos por gotas',
            'site_header': 'Administración de Manos por gotas',
            'title': 'Estadísticas de donaciones',
            'app_label': self.model._meta.app_label,
            'opts': self.model._meta,
            'has_change_permission': self.has_change_permission(request)
        }

        if request.method == "POST":
            form = FormularioEstadisticasDonacion(request.POST)
            if form.is_valid():
                anio = form.cleaned_data['anio']
                categoria = form.cleaned_data['categoria']
                titulo = "Donaciones por grupo sanguíneo del año {0!s}".format(anio)

                donacion_qs = Donacion.objects.filter(fechaHora__year=anio)

                queryset = donacion_qs\
                    .exclude(registro__donante__grupoSanguineo__isnull=True)\
                    .order_by('fechaHora')\
                    .extra(select={'mes': 'CAST(EXTRACT(month from "base_donacion"."fechaHora") AS INT)'})

                # Step 1: Create a DataPool with the data we want to retrieve.
                def meses_anio(x):
                    meses = {
                        "1": 'Enero',
                        "2": 'Febrero',
                        "3": 'Marzo',
                        "4": 'Abril',
                        "5": 'Mayo',
                        "6": 'Junio',
                        "7": 'Julio',
                        "8": 'Agosto',
                        "9": 'Septiembre',
                        "10": 'Octubre',
                        "11": 'Noviembre',
                        "12": 'Diciembre'
                    }

                    return (meses[x[0]],)

                if categoria == "mes":
                    donaciones = \
                        PivotDataPool(
                            series=[
                                {'options': {
                                'source': queryset,
                                'categories': 'mes',
                                'legend_by': 'registro__donante__grupoSanguineo__nombre'},
                                'terms': {
                                    'cantidad': Count('id')
                                    }}],
                                sortf_mapf_mts=(None, meses_anio, True))
                elif categoria == "gs":
                    donaciones = \
                        PivotDataPool(
                            series=[
                                {'options': {
                                    'source': queryset,
                                    'categories': 'registro__donante__grupoSanguineo__nombre'},
                                    'terms': {
                                        'cantidad': Count('id')
                                    }}],)
                else:
                    donaciones = \
                        PivotDataPool(
                            series=[
                                {'options': {
                                    'source': queryset,
                                    'categories': 'lugarDonacion__direccion__localidad__provincia__nombre'},
                                    'terms': {
                                        'cantidad': Count('id')
                                    }}], )

                # Step 2: Create the Chart object
                pivcht = PivotChart(
                    datasource=donaciones,
                    series_options=
                    [{'options': {
                        'type': 'column',
                        'stacking': True},
                        'terms': [
                            'cantidad'
                        ]}],
                    chart_options=
                    {'title': {
                        'text': titulo},
                     'xAxis': {
                        'text': 'Valores'},
                    })

                # Step 3: Send the chart object to the template.
                context['donaciones'] = pivcht

        else:
            form = FormularioEstadisticasDonacion()

        context['form'] = form

        context['adminform'] = admin.helpers.AdminForm(form, list([(None, {'fields': form.base_fields})]),
                                                       self.get_prepopulated_fields(request))
        return render(request, 'admin/base/donacion/estadisticas.html', context)

    empty_value_display = '--------'
    list_display = (
        'id',
        '_usuario',
        'estado_donacion',
        'foto',
        'fechaHora',
        'imagen_verificacion',
        'boton_verificacion'
    )

    inlines = [
        HistoricoEstadoDonacionInline,
    ]

    def estado_donacion(self, obj):
        return get_estado_donacion(obj)

    def boton_verificacion(self, obj):
        estado_donacion = get_estado_donacion(obj)
        if estado_donacion is not None and estado_donacion.lower() == ESTADO_PENDIENTE:
            link_verificacion = reverse('admin:base_donacion_verificar', args=[obj.id])
            link_rechazo = reverse('admin:base_donacion_rechazar', args=[obj.id])
            return "<a class='addlink' href='{0!s}' >Verificar</a> <a class='deletelink' href='{1!s}'>Rechazar</a>".format(
                link_verificacion,
                link_rechazo
            )
        else:
            return "--------"
    boton_verificacion.short_description = 'Verificar donación'
    boton_verificacion.allow_tags = True

    def _usuario(self, obj):
        return obj.registro.donante

    def _estadoDonacion(self, obj):
        return obj.historicoEstados.estado.nombre

admin.site.register(Donacion, DonacionAdmin)
