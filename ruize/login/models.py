from django.db import models

class Empleados(models.Model):
    dni_empl = models.CharField(primary_key=True, max_length=20)
    nombre_empl = models.CharField(max_length=100)
    apellido_empl = models.CharField(max_length=100)
    domicilio_empl = models.CharField(max_length=200)
    telefono_empl = models.CharField(max_length=15)
    correo_empl = models.EmailField()
    ROL_CHOICES = [
        ('cajero', 'Cajero'),
        ('gerente', 'Gerente'),
        ('admin', 'Admin'),
    ]
    rol_empl = models.CharField(max_length=20, choices=ROL_CHOICES)
    fecha_nacimiento_emp = models.DateField()

    def __str__(self):
        return f"{self.nombre_empl} {self.apellido_empl}"
        

class Login(models.Model):
    id_login = models.BigAutoField(primary_key=True)
    dni_empl = models.ForeignKey('Empleados', on_delete=models.CASCADE)
    usuario = models.CharField(max_length=50, unique=True)
    contraseña = models.CharField(max_length=255)
    ultimo_acceso = models.DateTimeField(null=True, blank=True)
    hs_login = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} - Último acceso: {self.ultimo_acceso}"
