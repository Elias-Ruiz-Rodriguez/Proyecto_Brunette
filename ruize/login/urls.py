# en login/urls.py
from django.urls import path
from . import views

app_name = 'login'
urlpatterns = [
    path('menu/', views.mostrar_menu, name='menu'),  # Define la URL de tu menú aquí
]
