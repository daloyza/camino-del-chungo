from django.contrib import admin

from .models import Favorito, Lugar

admin.site.register(Lugar)


@admin.register(Favorito)
class FavoritoAdmin(admin.ModelAdmin):
    list_display = ("lugar", "visitante", "fecha")
    list_filter = ("lugar",)
