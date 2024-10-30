from django.urls import reverse_lazy
from django.forms import formset_factory
from django.views.generic.edit import FormView
from django.utils import timezone
from django.shortcuts import get_object_or_404
from.forms import CajaForm, CajaUpdateForm
from .models import Caja, Mesas
from applications.cocina.models import Pedidos, DetallePedido, Productos
from .forms import PedidoForm, DetallePedidoForm
# Create your views here.


class AperturaCaja(FormView):

    form_class = CajaForm
    success_url = reverse_lazy('home_app:Index')
    template_name= 'caja/apertura_caja.html'


    def form_valid(self, form):
        user = self.request.user
        monto_inicial = form.cleaned_data['monto_inicial_caja']
        Caja.objects.crear_apertura_caja(user, monto_inicial)
        return super().form_valid(form)
    

    
class CierreCaja(FormView):
    form_class = CajaUpdateForm
    success_url = reverse_lazy('home_app:Index')
    template_name= 'caja/cierre_caja.html'


    def form_valid(self, form):
        user = self.request.user
        total_ingresos = form.cleaned_data['total_ingresos']
        total_egresos = form.cleaned_data['total_egresos']
        Caja.objects.cerrar_caja(user, total_ingresos, total_egresos)
        return super().form_valid(form)



class CrearPedidoView(FormView):
    template_name = 'caja/generar_pedido.html'
    form_class = PedidoForm
    success_url = reverse_lazy('home_app:Index')  # Redirige a la vista de éxito después de crear el pedido

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formPedido'] = DetallePedidoForm
        return context
    
    def form_valid(self, form):
            caja = get_object_or_404(Caja, abierta_caja=True)  # Caja abierta
            mesa = form.cleaned_data['mesa']
            tipo_pago = form.cleaned_data['tipo_pago_pedido']
            pagado = form.cleaned_data['pagado_pedido']
            pedido = Pedidos.objects.crear_pedidos(caja, mesa, tipo_pago, pagado)

            producto = self.request.POST.get('producto')
            producto_id =get_object_or_404(Productos, id=producto)
            total_pedido = self.request.POST.get('total_pedido')
            DetallePedido.objects.crear_detalleP(pedido, producto_id, total_pedido)


            return super().form_valid(form)


    # # Formset para manejar múltiples productos en un solo pedido
    # detalle_pedido_formset = formset_factory(DetallePedidoForm, extra=1, can_delete=False)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['formset'] = self.detalle_pedido_formset()
    #     return context

    # def form_valid(self, form):
    #     formset = self.detalle_pedido_formset(self.request.POST)
    #     print(formset)
    #     if formset.is_valid():
    #         # Crear el pedido principal
    #         caja = get_object_or_404(Caja, abierta_caja=True)  # Caja abierta
    #         mesa = form.cleaned_data['mesa']
    #         tipo_pago = form.cleaned_data['tipo_pago_pedido']
    #         pagado = form.cleaned_data['pagado_pedido']
    #         pedido = Pedidos.objects.crear_pedidos(caja, mesa, tipo_pago, pagado)
            
    #         # Guardar cada detalle del pedido
    #         for detalle_form in formset:
    #             print(detalle_form.cleaned_data.get('producto'))
    #             producto = detalle_form.cleaned_data.get('producto')
    #             total_pedido = detalle_form.cleaned_data.get('total_pedido')
    #             if producto and total_pedido:
    #                 DetallePedido.objects.crear_detalleP(pedido,producto, total_pedido)
    #         # Mesas.objects.update_mesa(mesa)


    #         return super().form_valid(form)
    #     else:
    #         return self.form_invalid(form)
