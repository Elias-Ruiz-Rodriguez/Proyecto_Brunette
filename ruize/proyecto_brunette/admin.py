from django.contrib import admin
from .models import Empleados, Login, Caja, Proveedores, Compras, Productos, DetalleCompra, Clientes, Ventas, DetalleVenta, PagoImpuestos, Impuestos, ProvProductos, Pedidos

admin.site.register(Empleados)
admin.site.register(Login)
admin.site.register(Caja)
admin.site.register(Proveedores)
admin.site.register(Compras)
admin.site.register(Productos)
admin.site.register(DetalleCompra)
admin.site.register(Clientes)
admin.site.register(Ventas)
admin.site.register(DetalleVenta)
admin.site.register(PagoImpuestos)
admin.site.register(Impuestos)
admin.site.register(ProvProductos)
admin.site.register(Pedidos)