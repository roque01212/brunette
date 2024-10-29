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

]