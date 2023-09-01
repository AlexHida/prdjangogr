from django import forms
from .models import Estudiante

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        exclude = ['asistencia']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.asistencia = 0

        self.fields['usua'].initial = ''
        self.fields['pass1'].initial = ''

        self.fields['nombre'].label = ''
        self.fields['apellido'].label = ''
        self.fields['correo'].label = ''
        self.fields['usua'].label = ''
        self.fields['pass1'].label = ''

    def clean_usua(self):
        usua = self.cleaned_data.get('usua')
        if Estudiante.objects.filter(usua=usua).exists():
            raise forms.ValidationError('Este usuario ya está registrado')

    
    def clean_correo(self):
        email = self.cleaned_data.get('correo')
        if Estudiante.objects.filter(correo=email).exists():
            raise forms.ValidationError('Este correo ya está registrado')