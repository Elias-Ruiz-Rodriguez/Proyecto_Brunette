from django import forms
from .models import Login

class LoginForm(forms.ModelForm):
    class Meta:
        model = Login
        fields = ['usuario', 'contraseña', 'dni_empl']  # Incluye solo los campos del modelo Login

    # Si necesitas incluir campos de la relación, puedes usar un formulario relacionado o personalizarlo:
    # Ejemplo: para acceder a 'rol_empl' a través de la relación con Empleados
    rol_empl = forms.CharField(max_length=100, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.dni_empl:
            self.fields['rol_empl'].initial = self.instance.dni_empl.rol_empl