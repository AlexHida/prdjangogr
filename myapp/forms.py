from django import forms
from .models import Estudiante

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        exclude = ['asistencia']  # Excluye el campo 'asistencia' del formulario

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.asistencia = 0  # Establece el valor por defecto de asistencia a 0

        fields = '__all__'  # Todos los campos del modelo