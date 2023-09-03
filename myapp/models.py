from django.db import models

# Create your models here.
class Estudiante(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.CharField(max_length=100)
    usua = models.CharField(max_length=50, default="guest")
    pass1 = models.CharField(max_length=100, default="guest") 
    TaGramar = models.IntegerField(verbose_name="TaGramar", default=0)
    TaPreguntas = models.IntegerField(verbose_name="TaPreguntas", default=0) 

    def __str__(self):
        return f"{self.nombre} {self.apellido}"