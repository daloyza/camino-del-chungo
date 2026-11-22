from django.db import models

class Lugar(models.Model):
    """Lugar histórico. Los 9 primeros los escribió el equipo (datos_lugares.json);
    el resto viene del catálogo de Monumentos Nacionales de IDE Patrimonio."""

    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    foto = models.ImageField(upload_to="lugares/", blank=True)
    latitud = models.FloatField()
    longitud = models.FloatField()

    # Datos de IDE Patrimonio (ver el comando importar_patrimonio)
    codigo_ide = models.CharField("código en IDE Patrimonio", max_length=30, unique=True, null=True, blank=True)
    categoria = models.CharField("categoría", max_length=60, blank=True)
    desde_ide = models.BooleanField("importado desde IDE Patrimonio", default=False)

    # Traducciones (opcionales): si están vacías se muestra el texto en español
    nombre_en = models.CharField("nombre en inglés", max_length=255, blank=True)
    descripcion_en = models.TextField("descripción en inglés", blank=True)
    nombre_pt = models.CharField("nombre en portugués", max_length=255, blank=True)
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
