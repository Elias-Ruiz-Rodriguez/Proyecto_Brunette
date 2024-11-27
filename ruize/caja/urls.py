from django.urls import path
from . import views

app_name = 'caja'

urlpatterns = [
    path('apertura/', views.apertura_caja, name='apertura_caja'),
    path('cierre/', views.cierre_caja, name='cierre_caja'),
    path('arqueo_caja/', views.arqueo_caja, name='arqueo_caja'),
]
