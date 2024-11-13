from django.contrib import admin
from django.urls import path, include
from login import views as login_views  # Importamos las vistas de login
from ventas import views as ventas_views  # Importamos las vistas de ventas
from caja import views as caja_views
from django.shortcuts import redirect  # Agregamos redirect para la redirección

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('inicio_sesion')),  # Redirige la raíz al inicio de sesión
    path('inicio_sesion/', login_views.inicio_sesion, name='inicio_sesion'),
    path('menu/', login_views.mostrar_menu, name='mostrar_menu'),
    path('registrar/', login_views.registrar_usuario, name='registrar_usuario'),
    path('registro/', login_views.verificar_datos, name='verificar_datos'),
    path('producto/', ventas_views.producto, name='producto'),
    path('producto/', include('ventas.urls')),
    path('pedido/', ventas_views.crear_pedido, name='pedido'),
    path('confirmar-pedido/', ventas_views.confirmar_pedido, name='confirmar_pedido'),
    path('caja/', include('caja.urls', namespace='caja')),
    path('caja/apertura', caja_views.apertura_caja, name='apertura_caja'),
    path('caja/cierre', caja_views.cierre_caja, name='cierre_caja'),
    path('login/', include('login.urls', namespace='login')),
    path('registro_prod/', ventas_views.registrar_producto, name='registro'),
    path('registro_producto/', ventas_views.registrar_producto, name='registro_producto'),
    path('ventas/', include('ventas.urls')),
]
