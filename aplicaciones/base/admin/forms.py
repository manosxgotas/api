from django import forms

import datetime

anio_actual = datetime.datetime.today().year

ANIOS_CHOICES = (
    (anio_actual, anio_actual),
    (anio_actual - 1, anio_actual - 1),
    (anio_actual - 2, anio_actual - 2),
)

GRUPOS_SANGUINEOS_CHOICES = (
    ('', 'Todos los grupos'),
    ('O+', 'O+'),
    ('A+', 'A+'),
    ('B+', 'B+'),
    ('AB+', 'AB+'),
    ('O-', 'O-'),
    ('A-', 'A-'),
    ('B-', 'B-'),
    ('AB-', 'AB-'),
)

CATEGORIA_SOLICITUDES_CHOICES = (
    (1, 'Por meses'),
    (2, 'Por cantidad de donantes')
)

CATEGORIA_DONACIONES_CHOICES = (
    ('mes', 'Por meses'),
    ('gs', 'Por grupo sanguíneo'),
    ('provincia', 'Por provincia')
)


class FormularioGenerarCodigos(forms.Form):
    cantidad_codigos = forms.IntegerField(min_value=1, label='Cantidad')
    dias_vigencia = forms.IntegerField(
        min_value=1,
        required=False,
        label='Días de vigencia a partir de hoy (por defecto 30 días)'
        )


class FormularioEstadisticasDonacion(forms.Form):
    anio = forms.ChoiceField(
        choices=ANIOS_CHOICES,
        label="Año",
        widget=forms.Select(attrs={'id': 'anio_select', 'class': 'form-control'})
    )
    categoria = forms.ChoiceField(
        choices=CATEGORIA_DONACIONES_CHOICES,
        label="Categoría de filtrado",
        widget=forms.Select(attrs={'id': 'categoria_select', 'class': 'form-control'})
    )


class FormularioEstadisticasSolicitudDonacion(forms.Form):
    anio = forms.ChoiceField(
        choices=ANIOS_CHOICES,
        label="Año",
        widget=forms.Select(attrs={'id': 'anio_select', 'class': 'form-control'})
    )

    gs = forms.ChoiceField(
        choices=GRUPOS_SANGUINEOS_CHOICES,
        label="Grupo sanguíneo",
        required=False,
        widget=forms.Select(attrs={'id': 'gs_select', 'class': 'form-control'})
    )

    categoria = forms.ChoiceField(
        choices=CATEGORIA_SOLICITUDES_CHOICES,
        label="Categoría de filtrado",
        widget=forms.Select(attrs={'id': 'categoria_select', 'class': 'form-control'})
    )
