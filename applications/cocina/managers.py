from django.db import models
from decimal import Decimal


class ProductosManager(models.Manager):
    pass

    
    


class DetallePedidoManager(models.Manager):

    def crear_detalleP(self, pedido, producto, total):
        
        subtotal = producto.precio_prod * Decimal(total)

        return self.create(
            pedido = pedido,
            producto = producto,
            total_pedido = total,
            subtotal = subtotal
        )
    

  
    
class PedidosManager(models.Manager):

    def crear_pedidos(self, caja, mesa, tipo_pago, pagado):
        return self.create(
            caja = caja,
            mesa = mesa,
            tipo_pago_pedido = tipo_pago,
            pagado_pedido = pagado
        )
    
    def pedidos_mesas(self, mesa):
        return self.filter(
            mesa = mesa,
            pedido_listo = False
        ).exists()
    