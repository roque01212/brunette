from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.forms import formset_factory
from django.views import View
from django.views.generic.edit import FormView
from django.views.generic import DeleteView, UpdateView, ListView
from django.utils import timezone
from django.shortcuts import get_object_or_404
from.forms import CajaForm, CajaUpdateForm
from .models import Caja, Mesas
from applications.cocina.models import Pedidos, DetallePedido, Productos
from applications.users.mixins import CajaPermisoMixin
from .forms import PedidoForm, DetallePedidoForm, DetallePedidoUpdateForm
# Create your views here.


class AperturaCaja(CajaPermisoMixin, FormView):

    form_class = CajaForm
    success_url = reverse_lazy('home_app:Index')
    template_name= 'caja/apertura_caja.html'


    def form_valid(self, form):
        user = self.request.user
        monto_inicial = form.cleaned_data['monto_inicial_caja']
        Caja.objects.crear_apertura_caja(user, monto_inicial)
        return super().form_valid(form)
    

    
class CierreCaja(CajaPermisoMixin, FormView):
    form_class = CajaUpdateForm
    success_url = reverse_lazy('home_app:Index')
    template_name= 'caja/cierre_caja.html'


    def form_valid(self, form):
        user = self.request.user
        total_ingresos = form.cleaned_data['total_ingresos']
        total_egresos = form.cleaned_data['total_egresos']
        Caja.objects.cerrar_caja(user, total_ingresos, total_egresos)
        return super().form_valid(form)


class CrearPedidoView(CajaPermisoMixin, FormView):
    template_name = 'caja/generar_pedido.html'
    form_class = PedidoForm
    success_url = reverse_lazy('caja_app:Crear_Pedido')

    def get_initial(self):
        # Inicializar valores de mesa y tipo de pago para mantenerlos al redirigir
        initial = super().get_initial()
        mesa_id = self.request.session.get('mesa')
        if mesa_id:
            initial['mesa'] = get_object_or_404(Mesas, id=mesa_id)  # Obtener la instancia de Mesa
        initial['tipo_pago_pedido'] = self.request.session.get('tipo_pago_pedido')
        initial['pagado_pedido'] = self.request.session.get('pagado_pedido')
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formPedido'] = DetallePedidoForm()
        context['lista_pedidos'] = DetallePedido.objects.filter(
            pedido__mesa__id = self.request.session.get('mesa')
        )
        context['form_update'] = DetallePedidoUpdateForm()
       
        return context

    def form_valid(self, form):
        # Obtener y guardar los datos del pedido principal
        caja = get_object_or_404(Caja, abierta_caja=True)
        mesa = form.cleaned_data['mesa']
        tipo_pago = form.cleaned_data['tipo_pago_pedido']
        pagado = form.cleaned_data['pagado_pedido']
        pedido = Pedidos.objects.crear_pedidos(caja, mesa, tipo_pago, pagado)

        # Guardar los datos de la mesa y el tipo de pago en la sesión
        self.request.session['mesa'] = mesa.id  # Almacenar solo el ID
        self.request.session['tipo_pago_pedido'] = tipo_pago
        self.request.session['pagado_pedido'] = pagado

        # Guardar el detalle del pedido
        producto = self.request.POST.get('producto')
        producto_id = get_object_or_404(Productos, id=producto)
        total_pedido = self.request.POST.get('total_pedido')
        
        
        DetallePedido.objects.crear_detalleP(pedido, producto_id, total_pedido)

        return redirect(self.success_url)  # Redirige a la misma página



class TerminarPedidoView(CajaPermisoMixin, View):

    

    def post(self, request, *args, **kwargs):
        id_mesa = request.session.get('mesa')
       
        if id_mesa:
            Mesas.objects.update_mesa(id_mesa)

        # Eliminar los datos de la sesión
        request.session.pop('mesa', None)
        request.session.pop('tipo_pago_pedido', None)
        request.session.pop('pagado_pedido', None)

        # Redirigir a la página de inicio
        return redirect(reverse_lazy('home_app:Index'))


class DetallePedidoDeleteView(CajaPermisoMixin, DeleteView):
    model = DetallePedido
    success_url = reverse_lazy('caja_app:Crear_Pedido')
      

class DetallePedidoUpdateView(CajaPermisoMixin,UpdateView):
    model = DetallePedido
    form_class = DetallePedidoUpdateForm
    template_name = 'caja/update.html'  # Asegúrate de que el template existe y tiene el formulario correcto
    success_url = reverse_lazy('caja_app:Crear_Pedido')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Verificar si la solicitud es AJAX usando el encabezado
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({"success": True}, status=200)
        return response

    def get(self, request, *args, **kwargs):
        # Usa get_object_or_404 para evitar un error si el objeto no existe
        self.object = get_object_or_404(DetallePedido, pk=kwargs['pk'])
        context = self.get_context_data()

        # Verificar si la solicitud es AJAX usando el encabezado
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string(self.template_name, context, request=request)
            return JsonResponse({"html": html}, status=200)

        # Si no es una solicitud AJAX, procesa normalmente
        return super().get(request, *args, **kwargs)
    



class MesasListView(ListView):
    model = Mesas
    template_name = 'caja/lista_mesas.html'
    context_object_name = 'mesas'


    
