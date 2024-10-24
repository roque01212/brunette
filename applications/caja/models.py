from django.db import models
from applications.users.models import User

# Create your models here.


class Caja(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    abierta_caja = models.BooleanField(default=False)
    fecha_hs_aper_caja = models.DateTimeField('Apertura caja', auto_now=False, auto_now_add=False)
    fecha_hs_cierre_caja = models.DateTimeField('Cierre caja', auto_now=False, auto_now_add=False)
    monto_inicial_caja = models.DecimalField('Monto inicial', max_digits=10, decimal_places=2)
    total_ingresos = models.DecimalField('Total Ingreso', max_digits=10, decimal_places=2)
    total_egresos = models.DecimalField('Total Egreso', max_digits=10, decimal_places=2)
    total_caja= models.DecimalField('Total caja', max_digits=10, decimal_places=2)

    class Meta:
        """Meta definition for Caja."""

        verbose_name = 'Caja'
        verbose_name_plural = 'Cajas'

    def __str__(self):
        return f"{self.user.full_name} {self.monto_inicial_caja}"
    