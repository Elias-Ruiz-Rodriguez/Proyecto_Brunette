from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect,JsonResponse
from django.contrib import messages
from django.utils import timezone
from .models import Producto, Pedido, DetallePedido
from .forms import ProductoForm
from decimal import Decimal
import json
from caja.models import Caja, MovimientoCaja
from login.models import Login


def registrar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/producto')
    else:
        form = ProductoForm()

    return render(request, 'registrar/registro_producto.html', {'form': form})

def editar_producto(request):
    if request.method == 'POST':
        producto_id = request.POST.get('producto_id')

        # Verificar si `producto_id` está presente
        if not producto_id:
            messages.error(request, 'El ID del producto no fue proporcionado.')
            return redirect('producto')

        # Intentar obtener el producto
        try:
            producto = get_object_or_404(Producto, id_prod=producto_id)
        except Exception as e:
            messages.error(request, f'Error al encontrar el producto: {e}')
            return redirect('producto')

        # Obtener los valores del formulario
        nuevo_precio = request.POST.get('precio_prod')
        nueva_cantidad = request.POST.get('stock_prod')

        # Validar que los valores sean válidos
        if nuevo_precio and (nueva_cantidad or nueva_cantidad == ''):
            try:
                # Actualizar precio si es válido
                if nuevo_precio:
                    producto.precio_prod = Decimal(nuevo_precio)

                # Validar y actualizar stock solo si aplica
                if producto.stock_actual_prod is not None:
                    if nueva_cantidad == '':
                        messages.error(request, 'El stock no puede estar vacío para este producto.')
                    else:
                        nueva_cantidad = int(nueva_cantidad)
                        if nueva_cantidad < producto.stock_actual_prod:
                            messages.error(request, 'No se puede reducir el stock actual.')
                        else:
                            producto.stock_actual_prod = nueva_cantidad
                elif nueva_cantidad:
                    # Si el producto no tiene stock_actual_prod, no debería actualizarse
                    messages.error(request, 'Este producto no admite cambios en el stock.')

                producto.save()
                messages.success(request, 'Producto actualizado correctamente.')

            except (ValueError, Decimal.InvalidOperation) as e:
                messages.error(request, f'Error en los datos ingresados: {e}')
        else:
            messages.error(request, 'Por favor ingresa datos válidos.')

        return redirect('producto') 

    # Si no es un POST, redirigir
    return redirect('producto') 

def crear_pedido(request):
    productos = Producto.objects.all()

    # Obtener el ID del usuario logueado desde la sesión
    user_id = request.session.get('usuario_id')
    if not user_id:
        messages.error(request, "No has iniciado sesión.")
        return redirect('inicio_sesion')

    # Obtener la instancia de Login correspondiente
    usuario_logueado = Login.objects.filter(id_login=user_id).first()
    if not usuario_logueado:
        messages.error(request, "Usuario no válido.")
        return redirect('inicio_sesion')

    # Validar si hay una caja abierta
    caja = Caja.objects.filter(abierto=True).last()
    if not caja:
        messages.error(request, "No hay una caja abierta.")
        return redirect('inicio_sesion')

    if request.method == 'POST':
        if 'producto' in request.POST and 'cantidad' in request.POST and 'tipo_pago' in request.POST:
            producto_id = request.POST.get('producto')
            cantidad = request.POST.get('cantidad')
            tipo_pago = request.POST.get('tipo_pago')

            # Validar la cantidad ingresada
            if cantidad and cantidad.isdigit() and int(cantidad) > 0:
                producto = Producto.objects.get(id_prod=producto_id)
                cantidad = int(cantidad)

                # Crear el pedido con dni_empl relacionado al usuario logueado
                pedido = Pedido(
                    dni_empl=usuario_logueado,  # Relaciona al usuario logueado
                    id_caja=caja,  # Asociamos la caja abierta (objeto, no solo el id)
                    id_venta=1,  # Si es necesario, generar un ID de venta único
                    tipo_pago=tipo_pago,
                    fecha_gene_ped=timezone.now().date(),
                    hora_gen_ped=timezone.now().time(),
                )
                pedido.save()

                # Si es necesario, también podrías agregar el detalle del pedido (producto, cantidad, precio, etc.)
                # DetallePedido.objects.create(pedido=pedido, producto=producto, cantidad=cantidad, sub_total=...)

                return redirect('pedido_exito')

            error_message = "Por favor, ingresa una cantidad válida."
            return render(request, 'pedido/pedido.html', {'productos': productos, 'error_message': error_message})

    return render(request, 'pedido/pedido.html', {'productos': productos})

def confirmar_pedido(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            productos = data.get('productos', [])
            tipo_pago = data.get('tipo_pago')  
            total_pedido = 0

            # Obtener el ID del usuario logueado desde la sesión
            user_id = request.session.get('usuario_id')
            if not user_id:
                return JsonResponse({"success": False, "error": "No has iniciado sesión."})

            # Obtener la instancia de Login correspondiente
            usuario_logueado = Login.objects.filter(id_login=user_id).first()
            if not usuario_logueado:
                return JsonResponse({"success": False, "error": "Usuario no válido."})

            # Obtener la caja abierta
            caja = Caja.objects.filter(abierto=True).last()  # Obtener la última caja abierta
            if not caja:
                return JsonResponse({"success": False, "error": "No hay una caja abierta."})

            # Crear el pedido
            pedido = Pedido.objects.create(
                dni_empl=usuario_logueado,  # Relaciona al usuario logueado
                id_caja=caja,  # Asignamos la instancia de la caja abierta
                id_venta=1,  # ID de venta (puedes generarlo o asignarlo según tu lógica)
                generado_ped=True,
                fecha_gene_ped=timezone.now().date(),
                hora_gen_ped=timezone.now().time(),
                tipo_pago=tipo_pago
            )

            # Crear los detalles del pedido
            for producto_data in productos:
                producto = Producto.objects.get(id_prod=producto_data['id'])
                cantidad = producto_data['cantidad']
                precio_unitario = producto.precio_prod
                sub_total = precio_unitario * cantidad
                total_pedido += sub_total

                DetallePedido.objects.create(
                    id_pedido=pedido,
                    id_prod=producto,
                    precio_uni_ped=precio_unitario,
                    cant_ped=cantidad,
                    sub_total=sub_total,
                    total_ped=sub_total
                )

                # Actualizar el stock
                if producto.stock_actual_prod is not None:
                    producto.stock_actual_prod -= cantidad
                    producto.save()

            # Actualizar el total del pedido
            pedido.total_ped = total_pedido
            pedido.save()

            return JsonResponse({"success": True, "pedido_resumen": f"Total: ${total_pedido}"})
        except Exception as e:
            print(e)
            return JsonResponse({"success": False, "error": "Error al procesar el pedido."})

    return JsonResponse({"success": False, "error": "Método no permitido."})


def producto(request):
    rol_usuario = request.session.get('usuario_rol')

    if rol_usuario not in ["gerente", "admin"]:

        messages.error(request, "No tienes permisos para registrar usuarios.")
        return redirect('mostrar_menu')
    
    query = request.GET.get('product', '')  
    if query:
        productos = Producto.objects.filter(nombre_prod__icontains=query)
    else:
        productos = Producto.objects.all()
    
    usuario_nombre = request.session.get('usuario_nombre', 'Usuario desconocido')
    return render(request, 'producto/producto.html', {'productos': productos, 'usuario_nombre': usuario_nombre})

def ingreso_egreso(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        caja_id = data.get('caja_id')
        monto = Decimal(data.get('monto', 0))
        tipo = data.get('tipo')
        observaciones = data.get('observaciones', '')  # Observaciones opcionales

        try:
            # Obtener la caja
            caja = Caja.objects.get(id_caja=caja_id)

            if tipo == 'ingreso':
                caja.monto_actual += monto
                mensaje = "Ingreso realizado correctamente."
            elif tipo == 'egreso':
                if caja.monto_actual >= monto:
                    caja.monto_actual -= monto
                    mensaje = "Egreso realizado correctamente."
                else:
                    return JsonResponse({'success': False, 'message': 'No hay suficiente dinero en caja para el egreso.'})
            else:
                return JsonResponse({'success': False, 'message': 'Tipo de movimiento inválido.'})

            # Registrar el movimiento en MovimientoCaja
            MovimientoCaja.objects.create(
                caja=caja,
                tipo=tipo,
                monto=monto,
                observaciones=observaciones
            )

            # Guardar los cambios en la caja
            caja.save()

            return JsonResponse({'success': True, 'message': mensaje})

        except Caja.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Caja no encontrada.'})

    return JsonResponse({'success': False, 'message': 'Método no permitido.'})
