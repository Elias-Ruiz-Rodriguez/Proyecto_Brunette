from django.urls import path
from . import views

app_name = 'login'
urlpatterns = [
    path('caja/apertura', views.mostrar_caja, name='caja'),
    path('menu/', views.mostrar_menu, name='menu'), 
]
