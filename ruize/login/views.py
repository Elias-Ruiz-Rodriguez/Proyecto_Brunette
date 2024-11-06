from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Login
from django.contrib.auth import login as auth_login

def mi_vista(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Buscar el login por el username
            user_login = Login.objects.get(username=username)

            # Verificar si la contraseña es correcta
            if user_login.check_password(password):  # Usamos el método check_password para verificar
                # Si la autenticación es exitosa, hacer login con el empleado
                auth_login(request, user_login.dni_empleado)  # Autenticación estándar de Django
                return redirect('apertura_de_caja/apertura_de_caja.html')  # Redireccionar a la página correspondiente
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
        except Login.DoesNotExist:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'login/inicio_sesion.html')
