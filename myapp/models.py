from django.db import models

# Create your models here.
class Estudiante(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.CharField(max_length=100)
    usua = models.CharField(max_length=50, default="guest")
    pass1 = models.CharField(max_length=100, default="guest")  # No recomendado en producción, considera usar contraseñas seguras
    asistencia = models.IntegerField()

    def __str__(self):
        return f"{self.nombre} {self.apellido}"