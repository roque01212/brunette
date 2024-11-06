from django.urls import path

from . import views

app_name = "caja_app"

urlpatterns = [
    path(
        'caja/nueva-caja', 
        views.AperturaCaja.as_view(),
        name='Nueva_Caja',
    ),
    path(
        'caja/cierre-caja', 
        views.CierreCaja.as_view(),
        name='Cierre-caja',
    ),
    path('caja/crear-pedido/', 
         views.CrearPedidoView.as_view(), 
         name='Crear_Pedido'
    ),
    path('caja/eliminar-pedido/<pk>/', 
            views.DetallePedidoDeleteView.as_view(), 
            name='Eliminar_Pedido'
        ),
    path('caja/terminar-pedido/', 
         views.TerminarPedidoView.as_view(), 
         name='TerminarPedido'
    ),
    path('caja/actualizar-pedido/<pk>/', 
         views.DetallePedidoUpdateView.as_view(), 
         name='Actualizar_Pedido'),

    path('caja/lista-mesas/', 
         views.MesasListView.as_view(), 
         name='Lista_mesas'),
    
]