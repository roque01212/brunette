from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.views import View
from django.views.generic.edit import FormView
from django.views.generic import DeleteView, UpdateView, ListView
from django.shortcuts import get_object_or_404
from.forms import CajaForm, CajaUpdateForm
from .models import Caja, Mesas
from applications.cocina.models import Pedidos, DetallePedido, Productos
from applications.users.mixins import CajaPermisoMixin
from .forms import PedidoForm, DetallePedidoForm, DetallePedidoUpdateForm, PedidoForm2
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


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formPedido'] = DetallePedidoForm()

        context['lista_pedidos'] = DetallePedido.objects.filter(
                        pedido__pedido_listo = False
        ).order_by("-id")[:4]
        context['form_update'] = DetallePedidoUpdateForm()
       
        return context

    def form_valid(self, form):
        # Obtener y guardar los datos del pedido principal
        caja = get_object_or_404(Caja, abierta_caja=True)
        mesa = form.cleaned_data['mesa']
        tipo_pago = form.cleaned_data['tipo_pago_pedido']
        pagado = form.cleaned_data['pagado_pedido']
        pedido = Pedidos.objects.crear_pedidos(caja, mesa, tipo_pago, pagado)
        Mesas.objects.update_mesa(mesa.id)



        # Guardar el detalle del pedido
        producto = self.request.POST.get('producto')
        producto_id = get_object_or_404(Productos, id=producto)
        total_pedido = self.request.POST.get('total_pedido')
        
        
        DetallePedido.objects.crear_detalleP(pedido, producto_id, total_pedido)

        return redirect(self.success_url)  # Redirige a la misma página


def filtrar_productos(request):
    query = request.GET.get('kword'," ").strip() # Término de búsqueda
    if query:  # Si hay un término de búsqueda
        productos = Productos.objects.filter(nombre_prod__icontains=query)
    else:  # Si el término está vacío
        productos = Productos.objects.none() 
    data = [{'id': prod.id, 'nombre': prod.nombre_prod} for prod in productos]
    return JsonResponse({'productos': data})



# class CrearPedidoView(CajaPermisoMixin, FormView):
#     template_name = 'caja/generar_pedido.html'
#     form_class = PedidoForm
#     success_url = reverse_lazy('caja_app:Crear_Pedido')

#     def get_initial(self):
#         # Inicializar valores de mesa y tipo de pago para mantenerlos al redirigir
#         initial = super().get_initial()

#         mesa_id = self.request.session.get('mesa')
#         print(f"Mesa ID en sesión: {mesa_id}")  # Para verificar el valor
#         if mesa_id:
#             try:
#                 initial['mesa'] = Mesas.objects.get(id=mesa_id)  # Intentar obtener la mesa sin lanzar un error 404
#             except Mesas.DoesNotExist:
#                 print("No se encontró la mesa con el ID proporcionado.")
#                 self.request.session.pop('mesa', None)
#             initial['tipo_pago_pedido'] = self.request.session.get('tipo_pago_pedido')
#         initial['pagado_pedido'] = self.request.session.get('pagado_pedido')
#         return initial
    

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['formPedido'] = DetallePedidoForm()

#         context['lista_pedidos'] = DetallePedido.objects.filter(
#             pedido__mesa__id = self.request.session.get('mesa'),
#             pedido__pedido_listo = False
#         )
#         context['form_update'] = DetallePedidoUpdateForm()
       
#         return context

#     def form_valid(self, form):
#         # Obtener y guardar los datos del pedido principal
#         caja = get_object_or_404(Caja, abierta_caja=True)
#         mesa = form.cleaned_data['mesa']
#         tipo_pago = form.cleaned_data['tipo_pago_pedido']
#         pagado = form.cleaned_data['pagado_pedido']
#         pedido = Pedidos.objects.crear_pedidos(caja, mesa, tipo_pago, pagado)

#         # Guardar los datos de la mesa y el tipo de pago en la sesión
#         self.request.session['mesa'] = mesa.id  # Almacenar solo el ID
#         self.request.session['tipo_pago_pedido'] = tipo_pago
#         self.request.session['pagado_pedido'] = pagado

#         # Guardar el detalle del pedido
#         producto = self.request.POST.get('producto')
#         producto_id = get_object_or_404(Productos, id=producto)
#         total_pedido = self.request.POST.get('total_pedido')
        
        
#         DetallePedido.objects.crear_detalleP(pedido, producto_id, total_pedido)

#         return redirect(self.success_url)  # Redirige a la misma página


# class TerminarPedidoView(CajaPermisoMixin, View):

#     def post(self, request, *args, **kwargs):
#         id_mesa = request.session.get('mesa')
       
#         if id_mesa:
#             # Verificamos si existen detalles de pedidos para esta mesa
#             pedidos_activos = DetallePedido.objects.filter(
#                 pedido__mesa__id=id_mesa, 
#                 pedido__pedido_listo = False).exists()
#             if pedidos_activos:
#                 Mesas.objects.update_mesa(id_mesa)
#             # else:
#             #      Mesas.objects.activar_mesa(id_mesa)

#         # Eliminar los datos de la sesión
       
#         request.session.pop('mesa', None)
#         request.session.pop('tipo_pago_pedido', None)
#         request.session.pop('pagado_pedido', None)
#         # Redirigir a la página de inicio
#         return redirect(reverse_lazy('home_app:Index'))


class DetallePedidoDeleteView(CajaPermisoMixin, DeleteView):
    model = Pedidos
    success_url = reverse_lazy('caja_app:Crear_Pedido')

    def get_queryset(self):
        # Ordenar por ID descendente para mostrar del último al primero
        return DetallePedido.objects.all().order_by('id')

    

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
    
 

class PedidosListView(CajaPermisoMixin,ListView):
    model = DetallePedido
    template_name = "caja/pedidos.html"
    context_object_name='lista_pedidos'
    paginate_by= 9

    def get_queryset(self):
        # Mostrar todos los detalles de pedidos que no estén listos (categorías 0 y 1)
        return DetallePedido.objects.filter(
            pedido__pedido_listo=False,
            
        ).order_by('-id')


    


class MarcarPedidoListoView(CajaPermisoMixin,View):
    def post(self, request, pk, *args, **kwargs):
        pedido = get_object_or_404(Pedidos, id=pk)
        if not pedido.pedido_listo:  # Verifica que no esté marcado aún
            pedido.pedido_listo = True
            pedido.save()
        return redirect('caja_app:Lista_Pedidos')







class MesasListView(CajaPermisoMixin,ListView):
    model = Mesas
    template_name = 'caja/lista_mesas.html'
    context_object_name = 'mesas'

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mesas_con_pedidos_pendientes = Mesas.objects.filter(
            pedido_mesa__pagado_pedido=False
        ).distinct()
        context['cobrar'] = mesas_con_pedidos_pendientes
        return context

    


class MesasUpdateView(CajaPermisoMixin,UpdateView):
    model = Mesas
    fields = []  # Dejamos vacío porque no queremos mostrar un formulario completo
    success_url = reverse_lazy('caja_app:Lista_mesas')
    

    def post(self, request, *args, **kwargs):
        # Obtiene la mesa que se quiere actualizar
        mesa = get_object_or_404(Mesas, pk=kwargs['pk'])


        pedidos_pendientes = mesa.pedido_mesa.filter(
            Q(pagado_pedido=False) | Q(pedido_listo=False)
        )  # Asumiendo que hay un `related_name` 'pedido_mesa'

        if pedidos_pendientes.exists():
            return JsonResponse({'error': True, 'message': f'La mesa {mesa.num_mesa} tiene pedidos pendientes o aun no se no se pago'}, status=400)

        mesa.mesa_dispnible = True
        mesa.save()
        return JsonResponse({'success': True, 'message': f'La mesa {mesa.num_mesa} ha sido liberada correctamente.'})

    


class CobrarPedidosView(CajaPermisoMixin,View):

    def post(self, request, pk, *args, **kwargs):
        # Obtén la mesa que se desea cobrar
        mesa = get_object_or_404(Mesas, pk=pk)

        # Verifica si hay pedidos pendientes de pago para esta mesa
        pedidos_pendientes = mesa.pedido_mesa.filter(pagado_pedido=False)

        if pedidos_pendientes.exists():
            # Marcar todos los pedidos como pagados
            pedidos_pendientes.update(pagado_pedido=True)
            mesa.save()
        return redirect(reverse_lazy('caja_app:Lista_mesas'))
        
