from django.contrib import admin

from .models import Favorito, Lugar


@admin.register(Lugar)
class LugarAdmin(admin.ModelAdmin):
    list_display = ("nombre", "categoria", "desde_ide")
    list_filter = ("desde_ide", "categoria")
    search_fields = ("nombre",)


@admin.register(Favorito)
class FavoritoAdmin(admin.ModelAdmin):
    list_display = ("lugar", "visitante", "fecha")
    list_filter = ("lugar",)
