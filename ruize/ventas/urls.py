from django.urls import path
from . import views

urlpatterns = [
    # Otras rutas
    path('guardar_pedido/', views.guardar_pedido, name='guardar_pedido'),
]
