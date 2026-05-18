from django import forms
from django.forms import ModelChoiceField

from .models import EntradaProducto, Producto


class ProductoEntradaChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return f"[{obj.get_tipo_display()}] {obj.nombre} - {obj.categoria}"


class EntradaProductoForm(forms.ModelForm):

    producto = ProductoEntradaChoiceField(
        queryset=Producto.objects.filter(
            tipo__in=['enlatado', 'ingrediente'],
            activo=True
        ).order_by('tipo', 'categoria__nombre', 'nombre'),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = EntradaProducto
        fields = ['producto', 'cantidad', 'motivo']

        widgets = {
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0.01,
                'step': 0.01
            }),
            'motivo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ejemplo: entrada de mercancía del día'
            }),
        }
        
from .models import Producto


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'nombre',
            'categoria',
            'descripcion',
            'tipo',
            'unidad_medida',
            'precio',
            'stock',
            'activo',
        ]

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2
            }),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'unidad_medida': forms.Select(attrs={'class': 'form-select'}),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }