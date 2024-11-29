from django.urls import path

from . import views

app_name = "cocina_app"

urlpatterns = [
    path(
        'cocina/lista-mesas/', 
        views.MesasCocinaListView.as_view(),
        name='Mesas',
    ),
   path(
        'cocina/pedido-listo-cocina/<pk>/', 
        views.MarcarPedidoListoCocinaView.as_view(),
        name='Pedido_Listo_Cocina',
    ),
    path('cocina/productos/',
        views.ProductosListView.as_view(),
        name='Productos_List'
    ),
    path('cocina/crear/',
        views.ProductoCreateView.as_view(),
        name='Crear_Producto'
    ),
    path('cocina/editar/<pk>/',
        views.ProductoUpdateView.as_view(), 
        name='Editar_Producto'
    ),
     path('cocina/eliminar/<pk>/',
        views.ProductoDeleteView.as_view(), 
        name='Eliminar_Producto'
    ),

]