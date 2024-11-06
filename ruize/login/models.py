from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Empleados(models.Model):
    dni_empl = models.CharField(primary_key=True, max_length=20)
    nombre_empl = models.CharField(max_length=100)
    apellido_empl = models.CharField(max_length=100)
    domicilio_empl = models.CharField(max_length=200)
    telefono_empl = models.CharField(max_length=15)
    correo_empl = models.EmailField()
    ROL_CHOICES = [
        ('cajero', 'Cajero'),
        ('cocinero', 'Cocinero'),
        ('mesero', 'Mesero'),
        ('admin', 'Admin'),
    ]
    rol_empl = models.CharField(max_length=20, choices=ROL_CHOICES)
    fecha_nacimiento_emp = models.DateField()

    def __str__(self):
        return f"{self.nombre_empl} {self.apellido_empl}"

class Login(models.Model):
    id_login = models.BigAutoField(primary_key=True)
    dni_empl = models.ForeignKey('Empleados', on_delete=models.CASCADE)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)  # Aumentar el tamaño para contraseñas cifradas
    ultimo_acceso = models.DateTimeField(null=True, blank=True)
    hs_login = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.username} - Último acceso: {self.ultimo_acceso}"
