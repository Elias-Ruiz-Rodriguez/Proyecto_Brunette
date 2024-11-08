from django.contrib import admin
from .models import Caja

class CajaAdmin(admin.ModelAdmin):
    list_display = ['numero_caja', 'monto_apertura', 'fecha_apertura', 'usuario_apertura']
    readonly_fields = ['numero_caja']  # Esto asegura que no se pueda editar el campo 'numero_caja'

admin.site.register(Caja, CajaAdmin)
