from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Caja
from datetime import datetime
from django.contrib.auth.models import User

def apertura_caja(request):
    if request.method == 'POST':
        numero_caja = request.POST.get('numero_caja')
        monto_apertura = request.POST.get('monto_apertura')
        
        if numero_caja and monto_apertura:
            caja = Caja.objects.get(numero_caja=numero_caja)
            caja.monto_apertura = monto_apertura
            caja.monto_actual = monto_apertura
            caja.fecha_apertura = timezone.now()
            caja.usuario_apertura = request.user
            caja.abierto = True
            caja.save()
            
            return redirect('login:menu')  # Redirigir al menú principal
    
    # Obtener el listado de números de caja que están disponibles para abrir (donde `abierto=False`)
    cajas_disponibles = Caja.objects.filter(abierto=False).values_list('numero_caja', flat=True)
    
    # Generar cajas si no existen (esto solo ocurre la primera vez)
    if not Caja.objects.exists():
        for i in range(1, 11):
            Caja.objects.create(numero_caja=i, abierto=False)

    # Pasar la fecha actual y las cajas disponibles al template
    current_date = datetime.now().strftime('%d/%m/%Y')
    context = {
        'current_date': current_date,
        'cajas_disponibles': cajas_disponibles,
    }
    return render(request, 'caja/apertura.html', context)

def cierre_caja(request, caja_id):
    # Obtener la instancia de Caja específica
    caja = get_object_or_404(Caja, id=caja_id)
    
    if request.method == 'POST':
        # Si el formulario tiene un monto de dinero ingresado
        monto_ingresado = request.POST.get('ingreso_dinero')
        if monto_ingresado:
            caja.monto_actual += float(monto_ingresado)  # Actualizar el monto actual
            caja.save()

        # Al cerrar la caja, capturar la fecha y hora de cierre actual
        if 'cerrar_caja' in request.POST:
            caja.fecha_cierre = timezone.now()  # Guardar fecha y hora de cierre actual
            caja.monto_cierre = caja.monto_actual  # Registrar el monto actual como cierre
            caja.save()
            return redirect('home')  # Redirigir a una página de inicio o a donde desees
    
    return render(request, 'caja/cierre_caja.html', {'caja': caja})
