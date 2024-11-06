from django.urls import reverse_lazy
from django.forms import formset_factory
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
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
    

    
class CierreCaja(LoginRequiredMixin, FormView):
    form_class = CajaUpdateForm
    success_url = reverse_lazy('home_app:Index')
    template_name= 'caja/cierre_caja.html'
    login_url = reverse_lazy('users_app:User-Login')


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
            Mesas.objects.update_mesa(mesa)

            return super().form_valid(form)

