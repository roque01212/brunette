from django.db import models
from applications.caja.models import Caja, Mesas
from .managers import ProductosManager, DetallePedidoManager, PedidosManager
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
    mesa = models.ForeignKey(Mesas, on_delete=models.CASCADE, related_name='pedido_mesa')
    tipo_pago_pedido = models.CharField('Tipo de pago', max_length=2, choices=TIPO_PAGO_CHOICES)
    fecha_hs_pedido = models.DateTimeField(auto_now_add=True)
    pedido_listo = models.BooleanField(default=False)
    pagado_pedido = models.BooleanField(default=False)
    # image = models.ImageField('Imagen', upload_to='cocina', default='brunnete.jpg')


    objects = PedidosManager()

    class Meta:
        """Meta definition for Pedidos."""

        verbose_name = 'Pedidos'
        verbose_name_plural = 'Pedidoss'

    def __str__(self):
        return f"pedido de la mesa {self.mesa} fecha{self.fecha_hs_pedido}"
    
    def delete(self, *args, **kwargs):
        """
        Sobrescribe el método delete para restaurar el stock de los productos.
        """
        # Obtener los detalles relacionados usando el related_name 'pedido_detalle'
        detalles = self.pedido_detalle.all()
        for detalle in detalles:
            # Restaurar el stock del producto relacionado
            detalle.producto.stock_actual_prod += detalle.total_pedido
            detalle.producto.save()

        # Llamar al método delete original para eliminar el pedido
        super().delete(*args, **kwargs)
    
    


class Productos(models.Model):
    BEBIDA = '0'
    COCINA = '1'
    TIPO_CATEGORIA_CHOICES = [
        (BEBIDA, 'Bebida'),
        (COCINA, 'Cocina'),
    ]
    nombre_prod = models.CharField(max_length=100)
    precio_prod = models.DecimalField(max_digits=10, decimal_places=2)
    stock_min_prod = models.PositiveIntegerField(blank=True, null=True)  # Stock mínimo para alerta
    stock_actual_prod = models.PositiveIntegerField()  # Cantidad actual en stock
    existencia_insumo = models.BooleanField(default=True)  # Indica si el insumo está disponible
    categoria = models.CharField('Categoria', max_length=2, choices=TIPO_CATEGORIA_CHOICES)

    objects = ProductosManager()

    def __str__(self):
        return self.nombre_prod
    

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedidos, on_delete=models.CASCADE, related_name='pedido_detalle')
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    total_pedido = models.IntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)


    objects = DetallePedidoManager()
    class Meta:
        """Meta definition for DetallePedido."""

        verbose_name = 'DetallePedido'
        verbose_name_plural = 'DetallePedidos'

    def __str__(self):
        return f"{self.producto.nombre_prod} mesa {self.pedido.mesa.num_mesa}"

