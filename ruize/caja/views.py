from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Caja, HistorialCaja, MovimientoCaja
from login.models import Login
from ventas.models import Pedido
from decimal import Decimal
from django.contrib import messages


def apertura_caja(request):
    user_id = request.session.get('usuario_id') 

    if not user_id:
        messages.error(request, "No has iniciado sesión.")
        return redirect('inicio_sesion')

    try:
        usuario = Login.objects.get(id_login=user_id)
    except Login.DoesNotExist:
        messages.error(request, "Usuario no encontrado.")
        return redirect('inicio_sesion')

    # Buscamos o creamos la caja con un numero específico (usualmente será 1, pero el ID es único)
    caja, created = Caja.objects.get_or_create(numero_caja="1")  # Aseguramos que solo existe una caja con número 1
    
    if caja.abierto:
        messages.warning(request, "La caja ya está abierta. No es posible abrirla nuevamente.")
        return redirect('login:menu') 
    
    if request.method == 'POST':
        monto_apertura = request.POST.get('monto_apertura')
        if monto_apertura:
            # Abrimos la caja y asociamos los cambios
            caja.abrir(monto=Decimal(monto_apertura), usuario=usuario)

            # Creamos el historial de la caja
            HistorialCaja.objects.create(
                caja=caja,
                usuario=usuario,
                accion='apertura',
                monto_inicial=Decimal(monto_apertura),
                monto_final=caja.monto_actual,
                observaciones="Apertura de caja exitosa"
            )

            # Asociamos el ID de caja con los pedidos futuros
            # Si algún pedido es realizado después de esta apertura, tiene asociado el id_caja correcto
            messages.success(request, f"Caja {caja.numero_caja} abierta correctamente.")
            return redirect('login:menu')  

    current_date = timezone.now().strftime('%d/%m/%Y')
    return render(request, 'caja/apertura.html', {'current_date': current_date, 'caja': caja})

def cierre_caja(request):
    user_id = request.session.get('usuario_id') 
    if not user_id:
        messages.error(request, "No has iniciado sesión.")
        return redirect('inicio_sesion')

    try:
        usuario = Login.objects.get(id_login=user_id)
    except Login.DoesNotExist:
        messages.error(request, "Usuario no encontrado.")
        return redirect('inicio_sesion')

    caja = Caja.objects.filter(abierto=True).last()

    if not caja:
        messages.error(request, "No hay ninguna caja abierta.")
        return redirect('login:menu')

    if request.method == "POST":
        monto_efectivo_real = Decimal(request.POST.get('monto_efectivo_real', 0.00))
        monto_tarjeta_real = Decimal(request.POST.get('monto_tarjeta_real', 0.00))
        monto_ingreso = Decimal(request.POST.get('ingreso_dinero', 0.00))

        monto_final = caja.monto_actual + monto_ingreso

        caja.cerrar(monto_final, monto_efectivo_real, monto_tarjeta_real)

    
        HistorialCaja.objects.create(
            caja=caja,
            usuario=usuario, 
            accion='cierre',
            monto_inicial=caja.monto_actual,
            monto_final=monto_final,
            observaciones="Cierre de caja realizado correctamente"
        )

    
        messages.success(request, "Caja cerrada correctamente.")

        del request.session['usuario_id']  
        del request.session['usuario_nombre'] 

        return redirect('inicio_sesion')

    return render(request, 'caja/cierre_caja.html', {'caja': caja})

def arqueo_caja(request):
    # Obtener la caja que está abierta (asegurándonos de obtener la caja actual)
    caja_abierta = Caja.objects.filter(abierto=True).first()
    
    if not caja_abierta:
        # Si no hay una caja abierta, redirigimos a otra página o mostramos un mensaje
        return render(request, 'caja/no_caja_abierta.html')  # Puedes redirigir a una página de error

    # Obtener los pedidos realizados en la caja abierta
    pedidos = Pedido.objects.filter(id_caja=caja_abierta).select_related('dni_empl', 'dni_empl__dni_empl')
    
    # Obtener los movimientos de caja
    movimientos = MovimientoCaja.objects.filter(caja=caja_abierta)

    return render(request, 'caja/arqueo_caja.html', {
        'caja_abierta': caja_abierta,
        'pedidos': pedidos,
        'movimientos': movimientos,
    })