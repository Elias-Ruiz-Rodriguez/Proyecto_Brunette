from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.utils import timezone
from .models import Producto, Pedido, DetallePedido
from .forms import ProductoForm
from decimal import Decimal


def registrar_producto(request):
    if request.method == 'POST':
        # Aquí podrías agregar la lógica para guardar el formulario en la base de datos
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/producto')  # Redirige después de registrar
    else:
        form = ProductoForm()

    return render(request, 'registrar/registro_producto.html', {'form': form})

def crear_pedido(request):
    productos = Producto.objects.all()
    
    # Procesar la selección inicial de productos
    if request.method == 'POST' and 'producto' in request.POST:
        producto_id = request.POST.get('producto')
        cantidad = request.POST.get('cantidad')
        
        if cantidad and cantidad.isdigit() and int(cantidad) > 0:
            producto = Producto.objects.get(id_prod=producto_id)
            cantidad = int(cantidad)
            # Redirigir de nuevo para actualizar la tabla o el modal
            return render(request, 'pedido/pedido.html', {'productos': productos})

        error_message = "Por favor ingresa una cantidad válida."
        return render(request, 'pedido/pedido.html', {'productos': productos, 'error_message': error_message})

    return render(request, 'pedido/pedido.html', {'productos': productos})



def producto(request):
    query = request.GET.get('product', '')  # Obtener el término de búsqueda
    if query:
        productos = Producto.objects.filter(nombre_prod__icontains=query)
    else:
        productos = Producto.objects.all()
    return render(request, 'producto/producto.html', {'productos': productos})