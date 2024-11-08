from django.db import models

class Caja(models.Model):
    monto_apertura = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    monto_actual = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fecha_apertura = models.DateTimeField(auto_now_add=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    monto_cierre = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Caja abierta el {self.fecha_apertura}"
