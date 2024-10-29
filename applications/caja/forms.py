from django import forms
from .models import Caja

class CajaForm(forms.ModelForm):
    class Meta:
        """Meta definition for MODELNAMEform."""

        model = Caja
        fields = ('monto_inicial_caja',)

    

    def clean(self):
        if not self.cleaned_data['monto_inicial_caja'] > 0 :
            self.add_error('monto_inicial_caja', 'El monto debe ser superior a 0')
        return super().clean()

class CajaUpdateForm(forms.ModelForm):
    """Form definition for CajaUpdate."""

    class Meta:
        """Meta definition for CajaUpdateform."""

        model = Caja
        fields = ('total_ingresos', 'total_egresos')
        widgets = {
            'total_ingresos': forms.NumberInput(
                attrs = {

                    'class': 'form-control',
                }
            ),

            'total_egresos': forms.NumberInput(
                attrs = {
                    'class': 'form-control',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Marcar campos como requeridos en el formulario
        self.fields['total_ingresos'].required = True
        self.fields['total_egresos'].required = True

    def clean_total_ingresos(self):
        total_ingreso = self.cleaned_data['total_ingresos']
        if total_ingreso <= 0:
            self.add_error('total_ingresos', 'El monto debe ser superior a 0')
        return total_ingreso 

    def clean_total_egresos(self):
        total_egreso = self.cleaned_data['total_egresos']
        if total_egreso <= 0:
            self.add_error('total_egresos', 'El monto debe ser superior a 0')
        return total_egreso