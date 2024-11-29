from django import forms
from .models import Productos

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Productos
        fields = ['nombre_prod', 'precio_prod', 'stock_actual_prod', 'categoria']
        widgets = {
            'nombre_prod': forms.TextInput(attrs={'class': 'form-control'}),
            'precio_prod': forms.NumberInput(attrs={'class': 'form-control'}),
            
            'stock_actual_prod': forms.NumberInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
        }