from django.db import models
from django.contrib.auth.models import User

class Caja(models.Model):
    monto_apertura = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    monto_actual = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fecha_apertura = models.DateTimeField(null=True, blank=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    monto_cierre = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    numero_caja = models.IntegerField(unique=True, blank=True, null=True)
    usuario_apertura = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    abierto = models.BooleanField(default=False)  # Campo para indicar si la caja está abierta

    def save(self, *args, **kwargs):
        if not self.numero_caja:
            # Buscar el siguiente número de caja disponible
            cajas_abiertas = Caja.objects.filter(abierto=True).count()
            self.numero_caja = cajas_abiertas + 1 if cajas_abiertas < 10 else None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Caja {self.numero_caja} abierta el {self.fecha_apertura}"
