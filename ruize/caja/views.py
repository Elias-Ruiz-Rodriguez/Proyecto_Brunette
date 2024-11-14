from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Caja, HistorialCaja
from login.models import Login
from datetime import datetime
from decimal import Decimal
from django.contrib import messages
from django.http import JsonResponse
import json

def apertura_caja(request):
    # Obtener el ID del usuario desde la sesión
    user_id = request.session.get('usuario_id')  # Obtener el ID del usuario logueado

    if not user_id:
        # Si no hay un usuario logueado, redirigir a la página de inicio de sesión
        messages.error(request, "No has iniciado sesión.")
        return redirect('inicio_sesion')

    try:
        # Obtener el usuario de Login usando el ID guardado en la sesión
        usuario = Login.objects.get(id_login=user_id)
    except Login.DoesNotExist:
        # Si el usuario no existe, redirigir a la página de inicio de sesión
        messages.error(request, "Usuario no encontrado.")
        return redirect('inicio_sesion')

    # Obtener o crear la instancia de Caja con el número de caja "1"
    caja, created = Caja.objects.get_or_create(numero_caja="1")
    
    # Verificar si la caja ya está abierta
    if caja.abierto:
        messages.warning(request, "La caja ya está abierta. No es posible abrirla nuevamente.")
        return redirect('login:menu')  # Redirigir a la página del menú o a otra vista adecuada
    
    if request.method == 'POST':
        monto_apertura = request.POST.get('monto_apertura')
        if monto_apertura:
            # Usamos el usuario obtenido de la sesión en lugar de request.user
            caja.abrir(monto=Decimal(monto_apertura), usuario=usuario)

            # Registrar el historial de apertura
            HistorialCaja.objects.create(
                caja=caja,
                usuario=usuario,
                accion='apertura',
                monto_inicial=Decimal(monto_apertura),
                monto_final=caja.monto_actual,
                observaciones="Apertura de caja exitosa"
            )

            messages.success(request, f"Caja {caja.numero_caja} abierta correctamente.")
            return redirect('login:menu')  # Redirigir al menú después de abrir la caja correctamente

    current_date = timezone.now().strftime('%d/%m/%Y')
    return render(request, 'caja/apertura.html', {'current_date': current_date, 'caja': caja})

def cierre_caja(request):
    # Obtener el ID del usuario desde la sesión
    user_id = request.session.get('usuario_id')  # Obtener el ID del usuario logueado

    if not user_id:
        # Si no hay un usuario logueado, redirigir a la página de inicio de sesión
        messages.error(request, "No has iniciado sesión.")
        return redirect('inicio_sesion')

    try:
        # Obtener el usuario de Login usando el ID guardado en la sesión
        usuario = Login.objects.get(id_login=user_id)
    except Login.DoesNotExist:
        # Si el usuario no existe, redirigir a la página de inicio de sesión
        messages.error(request, "Usuario no encontrado.")
        return redirect('inicio_sesion')

    # Obtener la última caja abierta (si la hay)
    caja = Caja.objects.filter(abierto=True).last()

    # Si no hay ninguna caja abierta, redirigimos o mostramos un error
    if not caja:
        messages.error(request, "No hay ninguna caja abierta.")
        return redirect('login:menu')

    if request.method == "POST":
        # Obtenemos los montos del formulario
        monto_efectivo_real = Decimal(request.POST.get('monto_efectivo_real', 0.00))
        monto_tarjeta_real = Decimal(request.POST.get('monto_tarjeta_real', 0.00))
        monto_ingreso = Decimal(request.POST.get('ingreso_dinero', 0.00))

        # Calculamos el monto final de la caja, que es el monto actual + lo ingresado
        monto_final = caja.monto_actual + monto_ingreso

        # Procedemos a cerrar la caja
        caja.cerrar(monto_final, monto_efectivo_real, monto_tarjeta_real)

        # Registrar el historial de cierre
        HistorialCaja.objects.create(
            caja=caja,
            usuario=usuario,  # Usamos el usuario obtenido de la sesión
            accion='cierre',
            monto_inicial=caja.monto_actual,
            monto_final=monto_final,
            observaciones="Cierre de caja realizado correctamente"
        )

        # Enviamos un mensaje de éxito
        messages.success(request, "Caja cerrada correctamente.")

        # Limpiar la sesión (eliminar usuario_id y otros datos de sesión)
        del request.session['usuario_id']  # Eliminar el ID de usuario
        del request.session['usuario_nombre']  # Eliminar el nombre de usuario si lo estás usando

        # Redirigir al inicio de sesión
        return redirect('inicio_sesion')

    return render(request, 'caja/cierre_caja.html', {'caja': caja})