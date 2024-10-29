from django.db import models
from applications.caja.models import Caja, Mesas

# Create your models here.

class Pedidos(models.Model):
    # tipo pago constantes
    TARJETA = '0'
    EFECTIVO = '1'
    TRANSFERENCIA = '2'
    OTRO = '3'

    TIPO_PAGO_CHOICES = [
        (TARJETA, 'Tarjeta'),
        (EFECTIVO, 'Efectivo'),
        (TRANSFERENCIA, 'Tranferecia'),
        (OTRO, 'Otro'),
    ]

    caja = models.ForeignKey(Caja, on_delete=models.CASCADE)
    mesa = models.ForeignKey(Mesas, on_delete=models.CASCADE)
    tipo_pago_pedido = models.CharField('Tipo de pago', max_length=2, choices=TIPO_PAGO_CHOICES)
    fecha_hs_pedido = models.DateTimeField(auto_now_add=True)
    entrega_pedido = models.BooleanField(default=False)
    pagado_pedido = models.BooleanField(default=False)


    class Meta:
        """Meta definition for Pedidos."""

        verbose_name = 'Pedidos'
        verbose_name_plural = 'Pedidoss'

    def __str__(self):
        return f"pedido de la mesa {self.mesa__num_mesa}"
    


class Productos(models.Model):
    nombre_prod = models.CharField(max_length=100)
    precio_prod = models.DecimalField(max_digits=10, decimal_places=2)
    stock_min_prod = models.PositiveIntegerField()  # Stock mínimo para alerta
    stock_actual_prod = models.PositiveIntegerField()  # Cantidad actual en stock
    existencia_insumo = models.BooleanField(default=True)  # Indica si el insumo está disponible


    def __str__(self):
        return self.nombre_prod
    

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedidos, on_delete=models.CASCADE)
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    total_pedido = models.IntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)


    class Meta:
        """Meta definition for DetallePedido."""

        verbose_name = 'DetallePedido'
        verbose_name_plural = 'DetallePedidos'

    def save(self, *args, **kwargs):
        # Calcula el subtotal automáticamente
        self.subtotal = self.total_pedido * self.producto.precio_prod
        super().save(*args, **kwargs)

