from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView
from .models import Pedidos, DetallePedido
from applications.users.mixins import CocinaPermisoMixin

# Create your views here.



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
        context['no_puede'] = self.request.user.is_superuser
        return context


class MarcarPedidoListoCocinaView(CocinaPermisoMixin,View):

    def post(self, request, pk, *args, **kwargs):
        pedido = get_object_or_404(Pedidos, id=pk)
        if not pedido.pedido_listo:  # Verifica que no esté marcado aún
            pedido.pedido_listo = True
            pedido.save()
        return redirect('cocina_app:Mesas')

