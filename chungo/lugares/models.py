from django.db import models

class Lugar(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    foto = models.ImageField(upload_to="lugares/")
    latitud = models.FloatField()
    longitud = models.FloatField()

    def __str__(self):
        return self.nombre
# Create your models here.
