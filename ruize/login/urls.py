from django.urls import path
from . import views

app_name = 'login'
urlpatterns = [
    path('caja/apertura', views.apertura_caja, name='caja'),
    path('menu/', views.mostrar_menu, name='menu'), 
    path('caja/cierre/<int:caja_id>/', views.cierre_caja, name='cierre_caja'),
    path('editar_empleado/', views.editar_empleado, name='editar_empleado'),
    path('eliminar_empleado/<int:empleado_id>/', views.eliminar_empleado, name='eliminar_empleado'),
]
