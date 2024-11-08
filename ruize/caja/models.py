from django.db import models
from django.contrib.auth.models import User

class Caja(models.Model):
    monto_apertura = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    monto_actual = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fecha_apertura = models.DateTimeField(auto_now_add=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    monto_cierre = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    numero_caja = models.IntegerField(unique=True, blank=True, null=True)
    usuario_apertura = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.numero_caja:
            # Si no tiene número de caja, asigna el siguiente número de caja disponible
            last_caja = Caja.objects.all().order_by('numero_caja').last()
            self.numero_caja = (last_caja.numero_caja + 1) if last_caja else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Caja {self.numero_caja} abierta el {self.fecha_apertura}"
