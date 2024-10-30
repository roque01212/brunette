from django.db import models
from django.utils import timezone
from django.db.models import F


class CajaManager(models.Manager):

    def crear_apertura_caja(self, user, monto_inicial):

        return self.create(
            user = user,
            monto_inicial_caja = monto_inicial
        )
    

    def cerrar_caja(self, user, total_ingresos, total_egresos):
        # Calcular el total de caja
        total_caja = F('monto_inicial_caja') + total_ingresos - total_egresos

        # Actualizar la instancia de caja
        self.filter(user=user, abierta_caja=True).update(
            abierta_caja=False,
            fecha_hs_cierre_caja=timezone.now(),
            total_ingresos=total_ingresos,
            total_egresos=total_egresos,
            total_caja=total_caja
        )

class MesasManager(models.Manager):

    def update_mesa(self, mesa):
        return self.filter(id = mesa.id).update(mesa_dispnible=False)
