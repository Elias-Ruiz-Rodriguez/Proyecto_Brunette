from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect,JsonResponse
from django.contrib import messages
from django.utils import timezone
from .models import Producto, Pedido, DetallePedido
from .forms import ProductoForm
from decimal import Decimal
import json



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

def editar_producto(request):
    if request.method == 'POST':
        producto_id = request.POST.get('producto_id')
        producto = get_object_or_404(Producto, id_prod=producto_id)

        # Obtener los nuevos valores del formulario
        nuevo_precio = request.POST.get('precio_prod')
        nueva_cantidad = request.POST.get('stock_prod')

        # Validar y actualizar
        if nuevo_precio and nueva_cantidad:
            producto.precio_prod = Decimal(nuevo_precio)
            producto.stock_actual_prod = int(nueva_cantidad)
            producto.save()

            messages.success(request, 'Producto actualizado correctamente.')
        else:
            messages.error(request, 'Por favor ingresa datos válidos.')

        return redirect('producto')  # Redirige a la página de productos

    return redirect('producto')  # Redirige a la página de productos si el método no es POST

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

def confirmar_pedido(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            productos = data.get('productos', [])
            total_pedido = 0

            # Crear el pedido
            pedido = Pedido.objects.create(
                id_emple=request.user.id,
                id_caja=1,
                id_venta=1,
                generado_ped=True,
                fecha_gene_ped=timezone.now().date(),
                hora_gen_ped=timezone.now().time(),
            )

            for producto_data in productos:
                producto = Producto.objects.get(id_prod=producto_data['id'])
                cantidad = producto_data['cantidad']
                precio_unitario = producto.precio_prod
                sub_total = precio_unitario * cantidad
                total_pedido += sub_total

                # Crear el detalle del pedido
                DetallePedido.objects.create(
                    id_pedido=pedido,
                    id_prod=producto,
                    precio_uni_ped=precio_unitario,
                    cant_ped=cantidad,
                    sub_total=sub_total,
                    total_ped=total_pedido
                )

                # Actualizar el stock del producto
                producto.stock_actual_prod -= cantidad
                producto.save()

            # Actualizar el total en el pedido
            pedido.total_ped = total_pedido
            pedido.save()

            return JsonResponse({"success": True, "pedido_resumen": f"Total: ${total_pedido}"})
        except Exception as e:
            print(e)
            return JsonResponse({"success": False, "error": "Error al procesar el pedido."})

    return JsonResponse({"success": False, "error": "Método no permitido."})



def producto(request):
    query = request.GET.get('product', '')  # Obtener el término de búsqueda
    if query:
        productos = Producto.objects.filter(nombre_prod__icontains=query)
    else:
        productos = Producto.objects.all()
    return render(request, 'producto/producto.html', {'productos': productos})