from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Login

def inicio_sesion(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        contraseña = request.POST.get('contraseña')
        
        # Intentar autenticar al usuario
        try:
            user = Login.objects.get(usuario=usuario)
            if user.contraseña == contraseña:  # Comparación directa sin cifrado
                # Autenticación exitosa
                messages.success(request, "Inicio de sesión exitoso")
                return redirect('menu/menu.html')  # Cambia 'apertura_de_caja' por la ruta que desees
            else:
                messages.error(request, "Contraseña incorrecta")
        except Login.DoesNotExist:
            messages.error(request, "Usuario no encontrado")
    
    return render(request, 'inicio_sesion/inicio_sesion.html')

#def menu(request):
