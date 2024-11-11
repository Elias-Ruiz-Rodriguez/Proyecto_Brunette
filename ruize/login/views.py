from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Login
from .models import Empleados
from django.utils import timezone


def inicio_sesion(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        contraseña = request.POST.get('contraseña')
        
        try:
            user = Login.objects.get(usuario=usuario)
            if user.contraseña == contraseña: 
                messages.success(request, "Inicio de sesión exitoso")
                return redirect('apertura_caja') 
            else:
                messages.error(request, "Contraseña incorrecta")
        except Login.DoesNotExist:
            messages.error(request, "Usuario no encontrado")
    
    return render(request, 'inicio_sesion/inicio_sesion.html')

def mostrar_caja(request):
    return render(request, 'caja/apertura.html')

def mostrar_menu(request):
    return render(request, 'menu/menu.html')

def registrar_usuario(request):
    if request.method == 'POST':
        nombre_empl = request.POST.get('nombre_empl')
        apellido_empl = request.POST.get('apellido_empl')
        usuario = request.POST.get('usuario')
        contraseña = request.POST.get('contraseña') 
        rol_empl = request.POST.get('rol_empl')
        correo_empl = request.POST.get('correo_empl')
        dni_empl = request.POST.get('dni_empl')
        domicilio_empl = request.POST.get('domicilio_empl')
        telefono_empl = request.POST.get('telefono_empl')
        fecha_nacimiento_emp = request.POST.get('fecha_nacimiento_emp')

        if Empleados.objects.filter(dni_empl=dni_empl).exists():
            messages.error(request, "El DNI ya está registrado.")
            return redirect('registrar.html')
        
        nuevo_empleado = Empleados(
            dni_empl=dni_empl,
            nombre_empl=nombre_empl,
            apellido_empl=apellido_empl,
            correo_empl=correo_empl,
            domicilio_empl=domicilio_empl,
            telefono_empl=telefono_empl,
            rol_empl=rol_empl,
            fecha_nacimiento_emp=fecha_nacimiento_emp
        )
        nuevo_empleado.save()

        nuevo_login = Login(
            dni_empl=nuevo_empleado,
            usuario=usuario,
            contraseña=contraseña, 
            hs_login=timezone.now() 
        )
        nuevo_login.save()     

        messages.success(request, "Usuario registrado exitosamente")
        return redirect('mostrar_menu')
    else:
            messages.error(request, "Error al registrar usuario. Revisa los datos ingresados.")
    
    return render(request, 'registrar/registrar.html')

def verificar_datos(request):
    empleados = Empleados.objects.all()
    
    for empleado in empleados:
        print("Empleado:", empleado.nombre_empl, empleado.apellido_empl)
        
        logins = Login.objects.filter(dni_empl=empleado.dni_empl)
        for login in logins:
            print("Login:", login.usuario, login.contraseña)
            
    return render(request, 'registro/registro_usuario.html', {'empleados': empleados, 'logins': logins})
