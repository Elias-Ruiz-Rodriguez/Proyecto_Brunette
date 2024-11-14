from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal

class Caja(models.Model):
    id_caja = models.AutoField(primary_key=True)
    numero_caja = models.IntegerField(unique=True)
    monto_apertura = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    monto_actual = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    monto_efectivo_real = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    monto_tarjeta_real = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    diferencia_efectivo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    diferencia_tarjeta = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fecha_apertura = models.DateTimeField(null=True, blank=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    monto_cierre = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    usuario_apertura = models.ForeignKey('login.Login', on_delete=models.SET_NULL, null=True, blank=True)
    abierto = models.BooleanField(default=False)

    def abrir(self, monto, usuario):
        self.monto_apertura = monto
        self.monto_actual = monto
        self.fecha_apertura = timezone.now()
        self.usuario_apertura = usuario
        self.abierto = True
        self.save()

    def cerrar(self, monto_final, monto_efectivo_real, monto_tarjeta_real):
        """Cierra la caja y registra el monto final y las diferencias."""
        self.monto_efectivo_real = monto_efectivo_real
        self.monto_tarjeta_real = monto_tarjeta_real
        self.diferencia_efectivo = monto_efectivo_real - self.monto_actual
        self.diferencia_tarjeta = monto_tarjeta_real - self.monto_actual
        self.monto_cierre = monto_final
        self.fecha_cierre = timezone.now()
        self.abierto = False
        self.save()

    def __str__(self):
        return f"Caja {self.numero_caja} - {'abierta' if self.abierto else 'cerrada'}"
    
class HistorialCaja(models.Model):
    CAJA_CHOICES = [
        ('apertura', 'Apertura'),
        ('cierre', 'Cierre'),
    ]
    caja = models.ForeignKey('Caja', on_delete=models.CASCADE)
    usuario = models.ForeignKey('login.Login', on_delete=models.CASCADE)
    accion = models.CharField(max_length=10, choices=CAJA_CHOICES)
    monto_inicial = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    monto_final = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    fecha = models.DateTimeField(auto_now_add=True)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_accion_display()} - Caja {self.caja.numero_caja} - {self.usuario}"
