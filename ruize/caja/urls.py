from django.urls import path
from . import views

app_name = 'caja'

urlpatterns = [
    path('apertura/', views.apertura_caja, name='apertura_caja'),
    path('cierre/<int:caja_id>/', views.cierre_caja, name='cierre_caja'),
]