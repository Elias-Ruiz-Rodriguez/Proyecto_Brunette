from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
<<<<<<< HEAD
from django.http import JsonResponse
=======
from .forms import LoginForm
>>>>>>> b92bfe2c465ba23357c57b03234a04e7d8b48c14
from django.utils import timezone
from .models import Login, Empleados
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

def inicio_sesion(request):
    inicio_exitoso = False 
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        contraseña = request.POST.get('contraseña')
        
        try:
<<<<<<< HEAD
            
            user = Login.objects.get(usuario=usuario)
            if user.contraseña == contraseña: 

                user.ultimo_acceso = timezone.now()
                user.save()

                request.session['usuario_nombre'] = f"{user.dni_empl.nombre_empl} {user.dni_empl.apellido_empl}"
                request.session['usuario_id'] = user.id_login 
                request.session['usuario_rol'] = user.dni_empl.rol_empl

                inicio_exitoso = True 
                return redirect('apertura_caja') 
            else:
                inicio_exitoso = False  
                messages.error(request, "Contraseña incorrecta.")
        except Login.DoesNotExist:
            inicio_exitoso = False 
=======
            user = Login.objects.get(usuario=usuario)
            if user.contraseña == contraseña:
                user.ultimo_acceso = timezone.now()
                user.save()
                request.session['usuario_nombre'] = f"{user.dni_empl.nombre_empl} {user.dni_empl.apellido_empl}"
<<<<<<< HEAD
                request.session['usuario_id'] = user.id_login
=======
                request.session['usuario_id'] = user.id_login  # Guardar el ID del usuario
>>>>>>> 95c831722305d8b6555b4ceec423ebb585f93d5d
                request.session['usuario_rol'] = user.dni_empl.rol_empl

                inicio_exitoso = True
                return redirect('apertura_caja')
            else:
                inicio_exitoso = False 
                messages.error(request, "Contraseña incorrecta.")
        except Login.DoesNotExist:
            inicio_exitoso = False
>>>>>>> b92bfe2c465ba23357c57b03234a04e7d8b48c14
            messages.error(request, "Usuario no encontrado.")
    
    return render(request, 'inicio_sesion/inicio_sesion.html', {'inicio_exitoso': inicio_exitoso})

def registrar_usuario(request):
    """Vista para manejar el registro de nuevos usuarios"""
    rol_usuario = request.session.get('usuario_rol')

    if rol_usuario not in ["Gerente", "Admin"]:
        messages.error(request, "No tienes permisos para registrar usuarios.")
        return redirect('mostrar_menu')
    
    if request.method == 'POST':
<<<<<<< HEAD
=======

>>>>>>> b92bfe2c465ba23357c57b03234a04e7d8b48c14
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

<<<<<<< HEAD
 
        if Empleados.objects.filter(dni_empl=dni_empl).exists():
            messages.error(request, "El DNI ya está registrado.")
            return redirect('registrar_usuario')  

       
=======
        if Empleados.objects.filter(dni_empl=dni_empl).exists():
            messages.error(request, "El DNI ya está registrado.")
            return redirect('registrar_usuario') 

>>>>>>> b92bfe2c465ba23357c57b03234a04e7d8b48c14
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

<<<<<<< HEAD
       
=======
>>>>>>> b92bfe2c465ba23357c57b03234a04e7d8b48c14
        nuevo_login = Login(
            dni_empl=nuevo_empleado,
            usuario=usuario,
            contraseña=contraseña,
            hs_login=timezone.now()
        )
        nuevo_login.save()

        messages.success(request, "Usuario registrado exitosamente")
<<<<<<< HEAD
        return redirect('mostrar_menu')  
    else:
        return render(request, 'registrar/registrar.html')


=======
        return redirect('mostrar_menu') 
    else:
        return render(request, 'registrar/registrar.html')
    
def lista_usuarios(request):
    logins = Login.objects.select_related('dni_empl').all()
    return render(request, 'registro/registro_usuario.html', {'logins': logins})

>>>>>>> b92bfe2c465ba23357c57b03234a04e7d8b48c14
def mostrar_menu(request):
    """Vista para mostrar el menú principal"""
    return render(request, 'menu/menu.html')

def verificar_datos(request):
    rol_usuario = request.session.get('usuario_rol')

    if rol_usuario not in ["Gerente", "Admin"]:
        messages.error(request, "No tienes permisos para registrar usuarios.")
        return redirect('mostrar_menu')
    
    # Obtener todos los logins y empleados
    empleados = Empleados.objects.all()
<<<<<<< HEAD
    logins = Login.objects.all()  # Obtener los logins asociados a los empleados

    # Pasar los logins al contexto
    return render(request, 'registro/registro.html', {'empleados': empleados, 'logins': logins})
=======
    logins = Login.objects.all() 
>>>>>>> b92bfe2c465ba23357c57b03234a04e7d8b48c14


def apertura_caja(request):
    """Vista para manejar la apertura de caja"""
<<<<<<< HEAD
   
=======
>>>>>>> b92bfe2c465ba23357c57b03234a04e7d8b48c14
    return render(request, 'caja/apertura.html')

def cierre_caja(request):
    """Vista para manejar el cierre de caja"""
<<<<<<< HEAD
    caja_id = 1  
=======
    caja_id = 1 
>>>>>>> b92bfe2c465ba23357c57b03234a04e7d8b48c14
    return render(request, 'caja/cierre_caja.html', {'caja_id': caja_id})
