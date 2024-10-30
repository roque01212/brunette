from django.contrib import admin
from .models import Pedidos, Productos, DetallePedido
admin.site.register(Pedidos)
admin.site.register(Productos)
admin.site.register(DetallePedido)

# Register your models here.
