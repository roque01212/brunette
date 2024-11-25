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
    path('caja/actualizar-detalle-pedido/<pk>/', 
         views.DetallePedidoUpdateView.as_view(), 
         name='Actualizar_Pedido'
     ),

    path('caja/lista-mesas/', 
         views.MesasListView.as_view(), 
         name='Lista_mesas'
    ),
    path('caja/update-mesas/<pk>/', 
         views.MesasUpdateView.as_view(), 
         name='Update_Mesa'
    ),
    path('filtrar-productos/', 
         views.filtrar_productos, 
        name='filtrar_productos'
    ),
    path('lista-pedidos/', 
         views.PedidosListView.as_view(), 
        name='Lista_Pedidos'
    ),
    path('marcar-pedido-listo/<pk>/',
        views.MarcarPedidoListoView.as_view(),
        name='Marcar_Pedido_Listo'
    ),
    path('cobrar-pedidos/<pk>/',
        views.CobrarPedidosView.as_view(),
        name='Cobrar_Pedidos'
        ),


    
]