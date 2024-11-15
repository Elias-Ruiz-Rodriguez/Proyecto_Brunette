from django.shortcuts import render, redirect
from django.contrib import messages

from django.utils import timezone
from .models import Login, Empleados
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

def inicio_sesion(request):
    inicio_exitoso = False  # Variable para detectar éxito
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        contraseña = request.POST.get('contraseña')
        
        try:
            # Intentamos obtener al usuario por el nombre de usuario
            user = Login.objects.get(usuario=usuario)
            if user.contraseña == contraseña:  # Compara la contraseña en texto plano
                # Actualizamos el campo 'ultimo_acceso' con la fecha y hora actual
                user.ultimo_acceso = timezone.now()
                user.save()

                # Almacenamos el ID del usuario y el nombre completo en la sesión
                request.session['usuario_nombre'] = f"{user.dni_empl.nombre_empl} {user.dni_empl.apellido_empl}"
                request.session['usuario_id'] = user.id_login  # Guardar el ID del usuario
                request.session['usuario_rol'] = user.dni_empl.rol_empl

                inicio_exitoso = True  # Marca el inicio como exitoso
                return redirect('apertura_caja')  # Redirige a la vista de apertura de caja
            else:
                inicio_exitoso = False  # Marca el inicio como fallido
                messages.error(request, "Contraseña incorrecta.")
        except Login.DoesNotExist:
            inicio_exitoso = False  # Marca el inicio como fallido
            messages.error(request, "Usuario no encontrado.")
    
    return render(request, 'inicio_sesion/inicio_sesion.html', {'inicio_exitoso': inicio_exitoso})

def registrar_usuario(request):
    """Vista para manejar el registro de nuevos usuarios"""
    rol_usuario = request.session.get('usuario_rol')

    if rol_usuario not in ["Gerente", "Admin"]:
        # Si el rol no es gerente o admin, mostrar mensaje de error y redirigir
        messages.error(request, "No tienes permisos para registrar usuarios.")
        return redirect('mostrar_menu')
    
    if request.method == 'POST':
        # Datos para el modelo Empleados
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

        # Validación para evitar duplicados en base al DNI
        if Empleados.objects.filter(dni_empl=dni_empl).exists():
            messages.error(request, "El DNI ya está registrado.")
            return redirect('registrar_usuario')  # Asegúrate de que esta URL está configurada

        # Crear el nuevo empleado
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

        # Crear el nuevo usuario para el login
        nuevo_login = Login(
            dni_empl=nuevo_empleado,
            usuario=usuario,
            contraseña=contraseña,
            hs_login=timezone.now()
        )
        nuevo_login.save()

        messages.success(request, "Usuario registrado exitosamente")
        return redirect('mostrar_menu')  # Redirige al menú principal
    else:
        return render(request, 'registrar/registrar.html')
    
def eliminar_empleado(request, empleado_id):
    empleado = get_object_or_404(Empleados, id=empleado_id)
    empleado.delete()
    messages.success(request, "Empleado eliminado exitosamente")
    return redirect('verificar_datos')

def editar_empleado(request):
    if request.method == 'POST':
        dni = request.POST.get('dni')
        field = request.POST.get('field')
        value = request.POST.get('value')
        
        try:
            empleado = Empleados.objects.get(dni_empl=dni)
            
            # Actualiza el campo en el modelo Empleados
            if field == 'nombre_empl':
                empleado.nombre_empl = value
            elif field == 'apellido_empl':
                empleado.apellido_empl = value
            elif field == 'domicilio_empl':
                empleado.domicilio_empl = value
            elif field == 'telefono_empl':
                empleado.telefono_empl = value
            elif field == 'correo_empl':
                empleado.correo_empl = value
            elif field == 'rol_empl':
                empleado.rol_empl = value
            elif field == 'fecha_nacimiento_emp':
                empleado.fecha_nacimiento_emp = value
            
            empleado.save()
            return JsonResponse({'status': 'success', 'message': 'Empleado actualizado correctamente.'})
        except Empleados.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Empleado no encontrado.'}, status=404)
    
    return JsonResponse({'status': 'error', 'message': 'Método no permitido.'}, status=405)
def mostrar_menu(request):
    """Vista para mostrar el menú principal"""
    return render(request, 'menu/menu.html')

def verificar_datos(request):
    rol_usuario = request.session.get('usuario_rol')

    if rol_usuario not in ["Gerente", "Admin"]:
        # Si el rol no es gerente o admin, mostrar mensaje de error y redirigir
        messages.error(request, "No tienes permisos para registrar usuarios.")
        return redirect('mostrar_menu')
    """Vista para verificar y mostrar datos de empleados y sus logins asociados"""
    empleados = Empleados.objects.all()
    logins = Login.objects.all()  # Obtenemos todos los logins para mostrar en la página

    return render(request, 'registro/registro_usuario.html', {'empleados': empleados, 'logins': logins})

def apertura_caja(request):
    """Vista para manejar la apertura de caja"""
    # Aquí puedes añadir lógica adicional para verificar el estado de la caja
    return render(request, 'caja/apertura.html')

def cierre_caja(request):
    """Vista para manejar el cierre de caja"""
    caja_id = 1  # Cambia esto por el ID real que necesites
    return render(request, 'caja/cierre_caja.html', {'caja_id': caja_id})
