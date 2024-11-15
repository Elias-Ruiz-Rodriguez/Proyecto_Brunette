from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect,JsonResponse
from django.contrib import messages
from django.utils import timezone
from .models import Producto, Pedido, DetallePedido
from .forms import ProductoForm
from decimal import Decimal
from django.contrib.auth.decorators import login_required
import json
from caja.models import Caja


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
    productos = Producto.objects.all()  # Traemos todos los productos disponibles

    # Verificamos si el usuario está autenticado (basado en la sesión)
    user_id = request.session.get('usuario_id')
    if not user_id:
        messages.error(request, "No has iniciado sesión.")
        return redirect('inicio_sesion')  # Redirigir al inicio de sesión si no hay usuario

    caja = Caja.objects.filter(abierto=True).last()

    if request.method == 'POST':
        # Procesamos la selección de productos
        if 'producto' in request.POST and 'cantidad' in request.POST and 'tipo_pago' in request.POST:
            producto_id = request.POST.get('producto')
            cantidad = request.POST.get('cantidad')
            tipo_pago = request.POST.get('tipo_pago')  # Aquí tomamos el valor de tipo_pago

            if cantidad and cantidad.isdigit() and int(cantidad) > 0:
                producto = Producto.objects.get(id_prod=producto_id)
                cantidad = int(cantidad)

                # Crear el pedido usando el ID de usuario de la sesión
                pedido = Pedido(
                    id_emple=user_id,  # Usamos el ID del usuario desde la sesión
                    id_caja=caja.id_caja,  # Suponiendo que la caja ya está seleccionada
                    id_venta=1,  # Aquí puedes poner la lógica real de venta
                    tipo_pago=tipo_pago  # Aquí guardamos el tipo de pago
                )
                pedido.save()

                # Aquí podrías agregar los productos al pedido (detalle del pedido)
                # Puedes ajustar la lógica para asociar los productos seleccionados al pedido.

                return redirect('pedido_exito')  # Redirige a la página de éxito

            error_message = "Por favor ingresa una cantidad válida."
            return render(request, 'pedido/pedido.html', {'productos': productos, 'error_message': error_message})

    return render(request, 'pedido/pedido.html', {
        'productos': productos,  # Lista de productos disponibles
    })

def confirmar_pedido(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            productos = data.get('productos', [])  # Lista de productos
            tipo_pago = data.get('tipo_pago')  # Obtener tipo de pago desde la solicitud
            total_pedido = 0

            # Verificar si el usuario está autenticado
            user_id = request.session.get('usuario_id')
            if not user_id:
                return JsonResponse({"success": False, "error": "No has iniciado sesión."})

            # Crear el pedido
            pedido = Pedido.objects.create(
                id_emple=user_id,  # Usamos el ID del usuario desde la sesión
                id_caja=1,  # Suponemos que la caja ya está seleccionada
                id_venta=1,  # Aquí puedes poner la lógica real de venta
                generado_ped=True,
                fecha_gene_ped=timezone.now().date(),
                hora_gen_ped=timezone.now().time(),
                tipo_pago=tipo_pago  # Aquí agregamos el tipo de pago al crear el pedido
            )

            # Para cada producto en la lista de productos, se crea un detalle de pedido
            for producto_data in productos:
                producto = Producto.objects.get(id_prod=producto_data['id'])  # Obtener el producto por ID
                cantidad = producto_data['cantidad']  # Cantidad de producto solicitado
                precio_unitario = producto.precio_prod  # Obtener el precio unitario del producto
                sub_total = precio_unitario * cantidad  # Calcular el subtotal para este producto
                total_pedido += sub_total  # Acumulamos el total del pedido

                # Crear un detalle de pedido para este producto
                DetallePedido.objects.create(
                    id_pedido=pedido,
                    id_prod=producto,
                    precio_uni_ped=precio_unitario,
                    cant_ped=cantidad,
                    sub_total=sub_total,
                    total_ped=sub_total  # El total del pedido es el subtotal para este producto
                )

                # Verificar si el producto tiene un stock válido y restar la cantidad
                if producto.stock_actual_prod is not None and not isinstance(producto.stock_actual_prod, str):
                    producto.stock_actual_prod -= cantidad  # Restamos la cantidad al stock
                    producto.save()  # Guardamos los cambios en el producto

            # Actualizar el total del pedido
            pedido.total_ped = total_pedido
            pedido.save()  # Guardamos el pedido con su total final

            # Actualizar la caja según el tipo de pago
            caja = Caja.objects.filter(id_caja=1).first()  # Verifica si la caja es la correcta
            if caja:
                if tipo_pago == "efectivo":
                    caja.monto_actual += total_pedido  # Sumar al monto_actual
                elif tipo_pago == "tarjeta":
                    caja.monto_tarjeta_real += total_pedido  # Sumar al monto_tarjeta_real
                else:
                    return JsonResponse({"success": False, "error": "Tipo de pago no válido."})

                caja.save()  # Guardamos los cambios en la caja

            return JsonResponse({"success": True, "pedido_resumen": f"Total: ${total_pedido}"})
        except Exception as e:
            print(e)
            return JsonResponse({"success": False, "error": "Error al procesar el pedido."})

    return JsonResponse({"success": False, "error": "Método no permitido."})


def producto(request):
    rol_usuario = request.session.get('usuario_rol')

    if rol_usuario not in ["Gerente", "Admin"]:
        # Si el rol no es gerente o admin, mostrar mensaje de error y redirigir
        messages.error(request, "No tienes permisos para registrar usuarios.")
        return redirect('mostrar_menu')
    
    query = request.GET.get('product', '')  # Obtener el término de búsqueda
    if query:
        productos = Producto.objects.filter(nombre_prod__icontains=query)
    else:
        productos = Producto.objects.all()
    
    # Obtener el nombre del usuario desde la sesión
    usuario_nombre = request.session.get('usuario_nombre', 'Usuario desconocido')
    return render(request, 'producto/producto.html', {'productos': productos, 'usuario_nombre': usuario_nombre})

def ingreso_egreso(request):
    if request.method == 'POST':
        # Obtener los datos del cuerpo de la solicitud
        data = json.loads(request.body)
        caja_id = data.get('caja_id')
        monto = Decimal(data.get('monto', 0))  # Convertir el monto a Decimal para evitar errores de precisión
        tipo = data.get('tipo')

        # Obtener la caja desde la base de datos
        try:
            caja = Caja.objects.get(id_caja=caja_id)  # Cambiado de 'id' a 'id_caja'

            # Operación de ingreso
            if tipo == 'ingreso':
                caja.monto_actual += monto
            # Operación de egreso
            elif tipo == 'egreso':
                if caja.monto_actual >= monto:  # Verificar si hay suficiente dinero para el egreso
                    caja.monto_actual -= monto
                else:
                    return JsonResponse({'success': False, 'message': 'No hay suficiente dinero en caja para el egreso.'})

            # Guardar los cambios en la caja
            caja.save()

            return JsonResponse({'success': True, 'message': f'{tipo.capitalize()} realizado correctamente.'})

        except Caja.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Caja no encontrada.'})

    return JsonResponse({'success': False, 'message': 'Método no permitido.'})
