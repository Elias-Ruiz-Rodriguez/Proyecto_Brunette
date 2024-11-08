from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Caja
from datetime import datetime
from django.shortcuts import render, redirect
from .models import Caja
from django.contrib.auth.models import User

def apertura_caja(request):
    if request.method == 'POST':
        monto_apertura = request.POST.get('monto_apertura')
        if monto_apertura:
            caja = Caja.objects.create(
                monto_apertura=monto_apertura,
                monto_actual=monto_apertura,
                fecha_apertura=timezone.now(),
                usuario_apertura=request.user  # Se asigna el usuario que está abriendo la caja
            )
            return redirect('caja:cierre_caja', caja_id=caja.id)
    
    # Obtenemos la fecha actual para mostrarla en el template
    current_date = datetime.now().strftime('%d/%m/%Y')
    caja = Caja.objects.filter(fecha_cierre__isnull=True).last()  # Obtener la última caja abierta
    context = {
        'current_date': current_date,
        'caja': caja  # Pasamos la última caja para mostrar el número de caja
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
