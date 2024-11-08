from django.shortcuts import render, redirect
from .models import Caja
from datetime import datetime

def apertura_caja(request):
    if request.method == 'POST':
        monto_apertura = request.POST.get('monto_apertura')
        if monto_apertura:
            caja = Caja(monto_apertura=monto_apertura, monto_actual=monto_apertura)
            caja.save()
            return redirect('caja:cierre_caja', caja_id=caja.id)
    return render(request, 'caja/apertura.html')

def cierre_caja(request, caja_id):
    caja = Caja.objects.get(id=caja_id)
    
    if request.method == 'POST':
        monto_ingresado = request.POST.get('ingreso_dinero')
        if monto_ingresado:
            caja.monto_actual += float(monto_ingresado)
            caja.save()

        # Al cerrar la caja
        if 'cerrar_caja' in request.POST:
            caja.fecha_cierre = datetime.now()
            caja.monto_cierre = caja.monto_actual
            caja.save()
            return redirect('home')  # Redirige a una página de inicio o a donde desees
    
    return render(request, 'caja/cierre_caja.html', {'caja': caja})
