from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Pedidos, DetallePedido
from applications.users.mixins import CocinaPermisoMixin, AdminPermisoMixin
from applications.users.models import User
from .models import Productos
from .forms import ProductoForm


class MesasCocinaListView(CocinaPermisoMixin,ListView):
    model = DetallePedido
    template_name = "cocina/lista_mesas.html"
    context_object_name='lista_pedidos'
    paginate_by= 9

    def get_queryset(self):
        # Mostrar todos los detalles de pedidos que no estén listos (categorías 0 y 1)
        return DetallePedido.objects.filter(
            pedido__pedido_listo=False,
            producto__categoria='1'
        ).order_by('id')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Determina si el usuario tiene permiso de cocina o es superusuario
        context['no_puede'] = self.request.user.ocupation == User.ADMINISTRADOR
        return context


class MarcarPedidoListoCocinaView(CocinaPermisoMixin,View):

    def post(self, request, pk, *args, **kwargs):
        pedido = get_object_or_404(Pedidos, id=pk)
        if not pedido.pedido_listo:  # Verifica que no esté marcado aún
            pedido.pedido_listo = True
            pedido.save()
        return redirect('cocina_app:Mesas')


class ProductosListView(AdminPermisoMixin, ListView):
    model = Productos
    template_name = 'cocina/productos_list.html'
    context_object_name = 'productos'
    paginate_by = 7  # Número de productos por página

    def get_queryset(self):
        queryset = super().get_queryset()
        categoria = self.request.GET.get('categoria')  # Capturar el filtro de la URL
        if categoria:
            queryset = queryset.filter(categoria=categoria)
        queryset = queryset.order_by('nombre_prod')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Productos.TIPO_CATEGORIA_CHOICES  # Enviar las categorías al template
        return context


class ProductoCreateView(AdminPermisoMixin, CreateView):
    model = Productos
    form_class = ProductoForm
    template_name = 'cocina/crear_producto.html'
    success_url = reverse_lazy('cocina_app:Productos_List')  # Redirige a la lista de productos después de crear


class ProductoUpdateView(AdminPermisoMixin, UpdateView):
    model = Productos
    form_class = ProductoForm
    template_name = 'cocina/editar_producto.html'
    success_url = reverse_lazy('cocina_app:Productos_List')


class ProductoDeleteView(AdminPermisoMixin, DeleteView):
    model = Productos
    template_name = 'cocina/eliminar_producto.html'
    success_url = reverse_lazy('cocina_app:Productos_List')  # Redirige a la lista tras eliminar

    def get_context_data(self, **kwargs):
        # Para pasar datos adicionales al contexto si es necesario
        context = super().get_context_data(**kwargs)
        context['producto'] = self.object
        return context