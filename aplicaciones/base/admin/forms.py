from django import forms


class FormularioGenerarCodigos(forms.Form):
    cantidad_codigos = forms.IntegerField(min_value=1, label='Cantidad')
    dias_vigencia = forms.IntegerField(min_value=1, required=False,
        label='Días de vigencia a partir de hoy (por defecto 30 días)')
