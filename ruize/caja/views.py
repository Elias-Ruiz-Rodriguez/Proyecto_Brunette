from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Caja
from datetime import datetime
from django.contrib.auth.models import User
from decimal import Decimal
from django.contrib import messages
from django.http import JsonResponse
import json

def apertura_caja(request):
    # Asegurar que existe una instancia de Caja con el número de caja "001"
    caja, created = Caja.objects.get_or_create(numero_caja="001")
    
    if request.method == 'POST':
        monto_apertura = request.POST.get('monto_apertura')
        if monto_apertura:
            caja.abrir(monto=Decimal(monto_apertura), usuario=request.user)
            messages.success(request, f"Caja {caja.numero_caja} abierta correctamente.")
            # Redirigir al menú pasando el id de la caja (en lugar del numero_caja)
            return redirect('login:menu')  # Se redirige a la página del menú

    current_date = timezone.now().strftime('%d/%m/%Y')
    return render(request, 'caja/apertura.html', {'current_date': current_date, 'caja': caja})

def cierre_caja(request, caja_id):
    caja = get_object_or_404(Caja, id=caja_id)

    if request.method == "POST":
        # Obtenemos los montos del formulario
        monto_efectivo_real = Decimal(request.POST.get('monto_efectivo_real', 0.00))
        monto_tarjeta_real = Decimal(request.POST.get('monto_tarjeta_real', 0.00))
        monto_ingreso = Decimal(request.POST.get('ingreso_dinero', 0.00))

        # Calculamos el monto final de la caja, que es el monto actual + lo ingresado
        monto_final = caja.monto_actual + monto_ingreso

        # Procedemos a cerrar la caja
        caja.cerrar(monto_final, monto_efectivo_real, monto_tarjeta_real)

        # Enviamos un mensaje de éxito
        messages.success(request, "Caja cerrada correctamente.")

        # Redirigimos a alguna página (por ejemplo, al menú de inicio)
        return redirect('login:menu')

    return render(request, 'caja/cierre_caja.html', {'caja': caja})

def ingreso_egreso(request):
    if request.method == 'POST':
        # Obtener los datos del cuerpo de la solicitud
        data = json.loads(request.body)
        caja_id = data.get('caja_id')
        monto = data.get('monto')
        tipo = data.get('tipo')

        # Obtener la caja desde la base de datos
        try:
            caja = Caja.objects.get(id=caja_id)

            # Operación de ingreso
            if tipo == 'ingreso':
                caja.monto_efectivo_real += monto
            # Operación de egreso
            elif tipo == 'egreso':
                caja.monto_efectivo_real -= monto

            # Guardar los cambios
            caja.save()

            return JsonResponse({'success': True, 'message': f'{tipo.capitalize()} realizado correctamente.'})

        except Caja.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Caja no encontrada.'})

    return JsonResponse({'success': False, 'message': 'Método no permitido.'})