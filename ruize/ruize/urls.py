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
from login import views as login_views  # Importamos las vistas de login
from ventas import views as ventas_views  # Importamos las vistas de ventas
from caja import views as caja_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('inicio_sesion/', login_views.inicio_sesion, name='inicio_sesion'),
    path('menu/', login_views.mostrar_menu, name='mostrar_menu'),
    path('registrar/', login_views.registrar_usuario, name='registrar_usuario'),
    path('pedido/', ventas_views.pedido, name='pedido'),
    path('caja/', include('caja.urls', namespace='caja')),
    path('caja/apertura', caja_views.apertura_caja, name='apertura'),
    path('caja/cierre', caja_views.cierre_caja, name='ciere'),
]
