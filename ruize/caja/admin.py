from django.contrib import admin
from .models import Caja,HistorialCaja

class CajaAdmin(admin.ModelAdmin):
    list_display = ['id_caja','numero_caja', 'monto_apertura', 'fecha_apertura', 'usuario_apertura']
    readonly_fields = ['numero_caja']  
    ordering = ['id_caja'] 

class HistorialCajaAdmin(admin.ModelAdmin):
    list_display = ('caja', 'usuario', 'accion', 'monto_inicial', 'monto_final', 'fecha', 'observaciones')
    list_filter = ('accion', 'caja', 'usuario')
    search_fields = ('caja__numero_caja', 'usuario__username', 'accion')
    ordering = ('-fecha',)
    date_hierarchy = 'fecha'

admin.site.register(Caja, CajaAdmin)
admin.site.register(HistorialCaja, HistorialCajaAdmin)
