from django.db import models

class Lugar(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    foto = models.ImageField(upload_to="lugares/")
    latitud = models.FloatField()
    longitud = models.FloatField()

    # Traducciones (opcionales): si están vacías se muestra el texto en español
    nombre_en = models.CharField("nombre en inglés", max_length=100, blank=True)
    descripcion_en = models.TextField("descripción en inglés", blank=True)
    nombre_pt = models.CharField("nombre en portugués", max_length=100, blank=True)
    descripcion_pt = models.TextField("descripción en portugués", blank=True)

    def __str__(self):
        return self.nombre

    def traducir(self, idioma):
        """Deja el nombre y la descripción en el idioma pedido en
        nombre_mostrado y descripcion_mostrada (no cambia la base de datos)."""
        self.nombre_mostrado = getattr(self, f"nombre_{idioma}", "") or self.nombre
        self.descripcion_mostrada = getattr(self, f"descripcion_{idioma}", "") or self.descripcion
        return self


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
