from django import forms
from productos.models import Producto


class AgregarProductoForm(forms.Form):

    producto = forms.ModelChoiceField(
        queryset=Producto.objects.filter(activo=True).order_by(
            'categoria__nombre',
            'nombre'
        ),
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    cantidad = forms.DecimalField(
        min_value=0.01,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'min': '0.01'
        })
    )


class ConfirmarVentaForm(forms.Form):

    folio = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    mesa = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    numero_personas = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control'
        })
    )

    dependiente = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    efectivo = forms.DecimalField(
        min_value=0,
        decimal_places=2,
        initial=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01'
        })
    )

    transferencia = forms.DecimalField(
        min_value=0,
        decimal_places=2,
        initial=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01'
        })
    )