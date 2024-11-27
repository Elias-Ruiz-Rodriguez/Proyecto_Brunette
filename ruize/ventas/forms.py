from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre_prod', 'precio_prod', 'categoria_prod', 'stock_min_prod', 'stock_actual_prod', 'stock_max_prod', 'existencia_insumo']
