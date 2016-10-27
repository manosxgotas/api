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
    ('meses', 'Por meses'),
    ('donantes', 'Por cantidad de donantes'),
    ('tipo', 'Por tipo de solicitud')

)

ETIQUETA_SOLICITUDES_CHOICES = (
    ('', 'Sin etiqueta'),
    ('tipo', 'Por tipo de solicitud')
)

CATEGORIA_DONACIONES_CHOICES = (
    ('mes', 'Por meses'),
    ('gs', 'Por grupo sanguíneo'),
    ('provincia', 'Por provincia'),
    ('edad', 'Por edades'),
    ('sexo', 'Por sexo'),
    ('estado', 'Por estado de la donación'),
)

ETIQUETA_DONACIONES_CHOICES = (
    ('', 'Sin etiqueta'),
    ('gs', 'Por grupo sanguíneo'),
    ('estado', 'Por estado de la donación')
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

    etiqueta = forms.ChoiceField(
        choices=ETIQUETA_DONACIONES_CHOICES,
        label="Etiqueta de filtrado",
        required=False,
        widget=forms.Select(attrs={'id': 'etiqueta_select', 'class': 'form-control'})
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

    etiqueta = forms.ChoiceField(
        choices=ETIQUETA_SOLICITUDES_CHOICES,
        label="Etiqueta de filtrado",
        required=False,
        widget=forms.Select(attrs={'id': 'etiqueta_select', 'class': 'form-control'})
    )
