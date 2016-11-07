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
    HistoricoEstadoDonacion,
    GENEROS,
    MESES
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
                etiqueta = form.cleaned_data['etiqueta']
                titulo = "Donaciones por grupo sanguíneo del año {0!s}".format(anio)

                donacion_qs = Donacion.objects\
                    .filter(fechaHora__year=anio)

                # Step 1: Create a DataPool with the data we want to retrieve.

                def grupos_etarios(x):
                    grupos = {
                        1: 'Menores de 18 años',
                        2: 'Entre 18 y 25 años',
                        3: 'Entre 25 y 30 años',
                        4: 'Entre 30 y 40 años',
                        5: 'Entre 40 y 50 años',
                        6: 'Entre 50 y 60 años',
                        7: 'Mayor de 60 años',
                    }

                    return (grupos[int(x[0])],)

                def meses_anio(x):
                    mes = int(x[0])
                    return (MESES[mes],)

                def nombres_generos(x):
                    return (GENEROS[x[0]],)

                legend_by = None
                sortf_mapf_mts = None

                if categoria == "mes":
                    categories = 'mes'
                    sortf_mapf_mts = (lambda x: (int(x[0]),), meses_anio, False)
                    queryset = donacion_qs\
                        .extra(select={'mes': 'CAST(EXTRACT(month from "base_donacion"."fechaHora") AS INT)'})

                elif categoria == "gs":
                    categories = 'registro__donante__grupoSanguineo__nombre'
                    queryset = donacion_qs\
                        .exclude(registro__donante__grupoSanguineo__isnull=True)

                elif categoria == "edad":
                    categories = 'edad'
                    sortf_mapf_mts = (lambda x: (int(x[0]),), grupos_etarios, False)
                    queryset = donacion_qs\
                        .exclude(registro__donante__nacimiento__isnull=True)\
                        .extra(select={
                            'edad':
                            """
                                SELECT
                                    CASE
                                        when CAST(date_part('year', age(nacimiento)) AS INT)<18 then 1
                                        when CAST(date_part('year', age(nacimiento)) AS INT)>=18 and CAST(date_part('year', age(nacimiento)) AS INT)<25 then 2
                                        when CAST(date_part('year', age(nacimiento)) AS INT)>=25 and CAST(date_part('year', age(nacimiento)) AS INT)<30 then 3
                                        when CAST(date_part('year', age(nacimiento)) AS INT)>=30 and CAST(date_part('year', age(nacimiento)) AS INT)<40 then 4
                                        when CAST(date_part('year', age(nacimiento)) AS INT)>=40 and CAST(date_part('year', age(nacimiento)) AS INT)<50 then 5
                                        when CAST(date_part('year', age(nacimiento)) AS INT)>=50 and CAST(date_part('year', age(nacimiento)) AS INT)<60 then 6
                                        when CAST(date_part('year', age(nacimiento)) AS INT)>=60 then 7
                                    END
                                from base_donante where base_donacion.registro_id = base_registrodonacion.id
                                and base_registrodonacion.donante_id = base_donante.id
                            """
                        })

                elif categoria == "estado":
                    categories = 'estado_donacion'
                    queryset = donacion_qs\
                        .exclude(historicoEstados__isnull=True)\
                        .extra(select={
                            'estado_donacion':
                                """
                                    select resultado.nombre from
                                    (select distinct tablas_historicos.donacion_id,
                                    est.nombre, max_date FROM base_estadodonacion est,
                                    base_historicoestadodonacion as tablas_historicos
                                    inner join (select donacion_id, MAX(inicio) as max_date
                                    from public.base_historicoestadodonacion group by donacion_id)a
                                    on a.donacion_id = tablas_historicos.donacion_id and a.max_date = inicio
                                    where est.id = tablas_historicos.estado_id and tablas_historicos.donacion_id = base_donacion.id) resultado
                                """
                        })

                elif categoria == "provincia":
                    categories = 'lugarDonacion__direccion__localidad__provincia__nombre'
                    queryset = donacion_qs

                elif categoria == "sexo":
                    categories = 'registro__donante__genero'
                    sortf_mapf_mts = (None, nombres_generos, False)
                    queryset = donacion_qs

                if etiqueta == "gs":
                    legend_by = 'registro__donante__grupoSanguineo__nombre'
                    if categoria != "gs":
                        queryset = queryset\
                            .exclude(registro__donante__grupoSanguineo__isnull=True)

                elif etiqueta == "estado":
                    legend_by = 'estado_donacion'
                    if categoria != "estado":
                        queryset = queryset\
                            .exclude(historicoEstados__isnull=True)\
                            .extra(select={
                                'estado_donacion':
                                    """
                                        select resultado.nombre from
                                        (select distinct tablas_historicos.donacion_id,
                                        est.nombre, max_date FROM base_estadodonacion est,
                                        base_historicoestadodonacion as tablas_historicos
                                        inner join (select donacion_id, MAX(inicio) as max_date
                                        from public.base_historicoestadodonacion group by donacion_id)a
                                        on a.donacion_id = tablas_historicos.donacion_id and a.max_date = inicio
                                        where est.id = tablas_historicos.estado_id and tablas_historicos.donacion_id = base_donacion.id) resultado
                                    """
                            })

                donaciones = \
                    PivotDataPool(
                        series=[
                            {'options': {
                                'source': queryset,
                                'categories': categories,
                                'legend_by': legend_by},
                                'terms': {
                                    'cantidad': Count('id')
                                }}],
                        sortf_mapf_mts=sortf_mapf_mts)

                # Step 2: Create the Chart object
                pivcht = PivotChart(
                    datasource=donaciones,
                    series_options=[
                        {'options': {
                            'type': 'column',
                            'stacking': True},
                            'terms': [
                            'cantidad'
                        ]}],
                    chart_options={
                        'title': {
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

    exclude = [
        'registro'
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
