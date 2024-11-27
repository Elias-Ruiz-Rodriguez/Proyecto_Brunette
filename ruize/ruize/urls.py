"""
URL configuration for ruize project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from login import views as login_views  
from ventas import views as ventas_views  
from caja import views as caja_views
from django.shortcuts import redirect  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('inicio_sesion')),
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
    path('caja/arqueo_caja', caja_views.arqueo_caja, name='arqueo_caja'),
    path('login/', include('login.urls', namespace='login')),
    path('registro_producto/', ventas_views.registrar_producto, name='registro_producto'),
    path('ventas/', include('ventas.urls')),
]