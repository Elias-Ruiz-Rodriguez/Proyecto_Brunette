from django.urls import path
from . import views

app_name = 'login'
urlpatterns = [
    path('caja/apertura', views.apertura_caja, name='caja'),
    path('menu/', views.mostrar_menu, name='menu'), 
    path('caja/cierre/<int:caja_id>/', views.cierre_caja, name='cierre_caja'),
    path('registro/', views.lista_usuarios, name='lista_usuarios'),
]
