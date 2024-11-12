from django.urls import path
from . import views

urlpatterns = [
    # Otras rutas
    path('guardar_pedido/', views.crear_pedido, name='guardar_pedido'),
    path('editar_producto/', views.editar_producto, name='editar_producto'),
]
