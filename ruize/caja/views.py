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

    caja, created = Caja.objects.get_or_create(numero_caja="1")
    
    if caja.abierto:
        messages.warning(request, "La caja ya está abierta. No es posible abrirla nuevamente.")
        return redirect('login:menu') 
    
    if request.method == 'POST':
        monto_apertura = request.POST.get('monto_apertura')
        if monto_apertura:
            caja.abrir(monto=Decimal(monto_apertura), usuario=usuario)

            HistorialCaja.objects.create(
                caja=caja,
                usuario=usuario,
                accion='apertura',
                monto_inicial=Decimal(monto_apertura),
                monto_final=caja.monto_actual,
                observaciones="Apertura de caja exitosa"
            )

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
    # Usamos prefetch_related para obtener los detalles de cada pedido
    pedidos = Pedido.objects.prefetch_related('detalles').select_related('dni_empl', 'dni_empl__dni_empl').all()
    movimientos = MovimientoCaja.objects.all()  # Obtenemos los movimientos de caja

    # Si quieres calcular el total del pedido por cada uno de los detalles
    for pedido in pedidos:
        pedido.total = sum(detalle.total_ped for detalle in pedido.detalles.all())

    return render(request, 'caja/arqueo_caja.html', {
        'pedidos': pedidos,
        'movimientos': movimientos
    })



