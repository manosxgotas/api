from datetime import date, timedelta

from django.contrib import admin
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf.urls import url

from .forms import FormularioGenerarCodigos

from ..models import CodigoVerificacion


class CodigoVerificacionAdmin(admin.ModelAdmin):

    # Método para agregar nueva url para generar códigos de verificación en el
    # sitio de administración.
    def get_urls(self):
        urls = super(CodigoVerificacionAdmin, self).get_urls()
        add_urls = [
            url(
                r'^generar/$',
                self.admin_site.admin_view(self.generar),
                name='base_codigoverificacion_generar',
            )
        ]
        return add_urls + urls

    # Método para generar códigos de verificación.
    def generar(self, request):
        context = {
            'site_title': 'Administración de Manos por gotas',
            'site_header': 'Administración de Manos por gotas',
            'title': 'Generar códigos de verificación',
            'app_label': self.model._meta.app_label,
            'opts': self.model._meta,
            'has_change_permission': self.has_change_permission(request)
        }

        if request.method == 'POST':
            form = FormularioGenerarCodigos(request.POST)
            if form.is_valid():
                cantidad = form.cleaned_data['cantidad_codigos']
                dias_vigencia = form.cleaned_data['dias_vigencia']
                for _ in range(cantidad):
                    if dias_vigencia is not None:
                        CodigoVerificacion.objects.create(
                            fechaVencimiento=date.today() + timedelta(
                                days=dias_vigencia
                                )
                            )
                    else:
                        CodigoVerificacion.objects.create()
                return HttpResponseRedirect(
                    reverse(
                        'admin:base_codigoverificacion_changelist'
                        )
                    )
        else:
            form = FormularioGenerarCodigos()

        context['form'] = form

        context['adminform'] = admin.helpers.AdminForm(form, list([(None, {'fields': form.base_fields})]),
                                                       self.get_prepopulated_fields(request))

        return render(request, 'admin/base/codigoverificacion/generar.html', context)

    empty_value_display = '--------'
    list_display = (
        'codigo',
        'fechaEmision',
        'fechaVencimiento'
    )

admin.site.register(CodigoVerificacion, CodigoVerificacionAdmin)
