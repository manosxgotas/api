# coding=utf-8

from django.contrib import admin
from django.conf.urls import url
from django.shortcuts import render
from django.db.models import Count
from chartit import PivotDataPool, PivotChart
from .grupoSanguineoSolicitud import GrupoSanguineoSolicitudInline
from .forms import FormularioEstadisticasSolicitudDonacion

from ..models import (
    SolicitudDonacion,
    ImagenSolicitudDonacion,
    MESES
    )


class ImagenSolicitudDonacionInline(admin.TabularInline):
    model = ImagenSolicitudDonacion


class SolicitudDonacionAdmin(admin.ModelAdmin):
    """
    Especificación de la representación de la solicitud de
     donación en la interfaz de administración.
    """

    def get_urls(self):
        urls = super(SolicitudDonacionAdmin, self).get_urls()
        add_urls = [
            url(
                r'^estadisticas/$',
                self.admin_site.admin_view(self.estadisticas),
                name='base_solicituddonacion_estadisticas',
            )
        ]
        return add_urls + urls

    def estadisticas(self, request):
        context = {
            'site_title': 'Administración de Manos por gotas',
            'site_header': 'Administración de Manos por gotas',
            'title': 'Estadísticas de solicitudes de donación',
            'app_label': self.model._meta.app_label,
            'opts': self.model._meta,
            'has_change_permission': self.has_change_permission(request)
        }

        if request.method == "POST":
            form = FormularioEstadisticasSolicitudDonacion(request.POST)
            if form.is_valid():
                anio = form.cleaned_data['anio']
                gs = form.cleaned_data['gs']
                categoria = form.cleaned_data['categoria']
                etiqueta = form.cleaned_data['etiqueta']
                titulo = "Solicitudes de donación por grupo sanguíneo del año {0!s}".format(anio)

                solicitud_donacion_qs = SolicitudDonacion.objects.filter(fechaPublicacion__year=anio)

                queryset = solicitud_donacion_qs\
                    .extra(select={'mes': 'CAST(EXTRACT(month from "base_solicituddonacion"."fechaPublicacion") AS INT)'})

                if gs:
                    titulo += ' del grupo {0!s}'.format(gs)
                    queryset = queryset\
                        .exclude(gruposSanguineos__isnull=True)\
                        .filter(gruposSanguineos__grupoSanguineo__nombre=gs)

                # Step 1: Create a DataPool with the data we want to retrieve.
                def meses_anio(x):
                    mes = int(x[0])
                    return (MESES[mes],)

                def cantidad_donantes(x):
                    cantidad_donantes = int(x[0])
                    donantes = {
                        "<5": 'Menos de 5',
                        "<10": 'Entre 5 y 10',
                        ">10": 'Más de 10',
                    }

                    if cantidad_donantes < 5:
                        cantidad = "<5"
                    elif cantidad_donantes >= 5 and cantidad_donantes < 10:
                        cantidad = "<10"
                    else:
                        cantidad = ">10"

                    return (donantes[cantidad],)

                sortf_mapf_mts = None
                legend_by = None

                if categoria == "meses":
                    categories = 'mes'
                    sortf_mapf_mts = (None, meses_anio, False)

                elif categoria == "donantes":
                    categories = 'donantesNecesarios'
                    sortf_mapf_mts = (None, cantidad_donantes, False)

                elif categoria == "tipo":
                    categories = 'tipo__nombre'

                if etiqueta == "centro":
                    legend_by = 'centroDonacion__nombre'

                elif etiqueta == "tipo":
                    legend_by = 'tipo__nombre'

                solicitudes = PivotDataPool(
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
                    datasource=solicitudes,
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
                        })

                # Step 3: Send the chart object to the template.
                context['solicitudes'] = pivcht

        else:
            form = FormularioEstadisticasSolicitudDonacion()

        context['form'] = form

        context['adminform'] = admin.helpers.AdminForm(form, list([(None, {'fields': form.base_fields})]),
                                                       self.get_prepopulated_fields(request))

        return render(request, 'admin/base/solicituddonacion/estadisticas.html', context)

    empty_value_display = '--------'
    list_display = (
        'id',
        'titulo',
        'fechaPublicacion',
        'tipo',
        'centroDonacion',
        'donantesNecesarios'
    )

    list_filter = (
        'tipo',
        'centroDonacion'
    )

    inlines = [
            ImagenSolicitudDonacionInline,
            GrupoSanguineoSolicitudInline
        ]

admin.site.register(SolicitudDonacion, SolicitudDonacionAdmin)
