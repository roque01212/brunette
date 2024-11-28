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

]