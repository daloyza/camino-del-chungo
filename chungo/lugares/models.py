from django.db import models

class Lugar(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    foto = models.ImageField(upload_to="lugares/")
    latitud = models.FloatField()
    longitud = models.FloatField()

    def __str__(self):
        return self.nombre


class Favorito(models.Model):
    # No hay cuentas de usuario: cada navegador recibe un código al azar (ver views.codigo_visitante)
    visitante = models.CharField(max_length=32)
    lugar = models.ForeignKey(Lugar, on_delete=models.CASCADE, related_name="favoritos")
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha"]
        constraints = [
            models.UniqueConstraint(fields=["visitante", "lugar"], name="favorito_unico"),
        ]

    def __str__(self):
        return f"{self.lugar} ({self.visitante[:8]})"
