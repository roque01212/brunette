from django import forms
from .models import Caja, Mesas
from applications.cocina.models import Pedidos, DetallePedido, Productos
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

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedidos
        fields = ['mesa', 'tipo_pago_pedido', 'pagado_pedido']

        widgets = {
            'mesa': forms.Select(
                attrs = {

                    'class': 'form-select mt-2',
                }
            ),
            'tipo_pago_pedido': forms.Select(
                attrs = {

                    'class': 'form-select mt-2',
                }
            ),
            'pagado_pedido': forms.CheckboxInput(
                attrs = {

                    'class': 'form-check-input ',
                }
            ),
            
            
            }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Filtrar solo las mesas disponibles
    #     self.fields['mesa'].queryset = Mesas.objects.filter(mesa_dispnible=True)
        
    #     # Set default value for 'mesa' if provided in initial
    #     if 'mesa' in self.initial:
    #         self.fields['mesa'].initial = self.initial['mesa']

class PedidoForm2(forms.ModelForm):
    class Meta:
        model = Pedidos
        fields = ['mesa', 'tipo_pago_pedido', 'pagado_pedido']

        widgets = {
            'mesa': forms.Select(
                attrs = {

                    'class': 'form-select',
                }
            ),
            'tipo_pago_pedido': forms.Select(
                attrs = {

                    'class': 'form-select ',
                }
            ),
            'pagado_pedido': forms.CheckboxInput(
                attrs = {

                    'class': 'form-check-input ',
                }
            ),
            
            
            }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo las mesas disponibles
        self.fields['mesa'].queryset = Mesas.objects.all()


class DetallePedidoForm(forms.Form):

    producto = forms.ModelChoiceField(
            queryset=Productos.objects.none(),  # No cargar productos al inicio
            label="Producto",
            widget=forms.Select(attrs={
                'required': 'required',
                'class': 'form-select mt-2',
                "id":"id_producto"
            })
            )
    total_pedido = forms.IntegerField(
            widget=forms.NumberInput(attrs={
                'type':'number',
                'required': 'required',
                'class': 'form-control mt-2',
                'min':'1',
                'value':'1',
                }),
            label='Cantidad'
        )
    

    
class DetallePedidoUpdateForm(forms.ModelForm):
    """Form definition for DetallePedido."""

    class Meta:
        """Meta definition for DetallePedidoform."""

        model = DetallePedido
        fields = ('producto', 'total_pedido')


