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
    path('caja/ventas-realizadas/', 
        views.ventas_realizadas,
        name='Ventas_Realizadas'
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
    path('caja/lista-pedidos/', 
         views.PedidosListView.as_view(), 
        name='Lista_Pedidos'
    ),
    path('caja/marcar-pedido-listo/<pk>/',
        views.MarcarPedidoListoView.as_view(),
        name='Marcar_Pedido_Listo'
    ),
    path('caja/cobrar-pedidos/<pk>/',
        views.CobrarPedidosView.as_view(),
        name='Cobrar_Pedidos'
    ),
    path('caja(mesa/<pk>/generar-pdf/'
        , views.GenerarPDFView.as_view(), 
        name='Generar_PDF'
    ),
    path('caja/ranking-semanal/',
        views.RankingTortaView.as_view(),
        name='Ranking_Semanal'
    ),
    path('caja/ranking-torta-pdf/',
        views.ranking_torta_pdf,
        name='ranking_torta_pdf'
    ),
    path('caja/lista-ventas/',
        views.ListaCajasView.as_view(),
        name='Lista_Ventas'
    ),
    path('caja/detalle-cajas/<pk>/',
        views.DetalleCajaView.as_view(),
        name='Detalle_Cajas'
    ),

    
]