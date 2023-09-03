from django import forms
from .models import Estudiante

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        exclude = ['TaGramar', 'TaPreguntas']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.TaGramar = 0
        self.instance.TaPreguntas = 0

        self.fields['usua'].initial = ''
        self.fields['pass1'].initial = ''

        self.fields['nombre'].label = 'Nombre:'
        self.fields['apellido'].label = 'Apellido:'
        self.fields['correo'].label = 'Gmail'
        self.fields['usua'].label = 'Usuario'
        self.fields['pass1'].label = 'Contraseña'

    def clean_usua(self):
        usua = self.cleaned_data.get('usua')
        if Estudiante.objects.filter(usua=usua).exists():
            raise forms.ValidationError('Este usuario ya está registrado.')
        return usua