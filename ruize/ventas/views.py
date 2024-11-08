from django.shortcuts import render
from .models import Producto

def pedido(request):
    query = request.GET.get('product', '')  # Obtener el término de búsqueda
    if query:
        productos = Producto.objects.filter(nombre_prod__icontains=query)
    else:
        productos = Producto.objects.all()
    return render(request, 'pedido/pedido.html', {'productos': productos})
