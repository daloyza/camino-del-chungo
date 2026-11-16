from django.urls import path
from . import views

urlpatterns = [
    path("", views.lista_lugares, name="lista"),
    path("lugar/<int:lugar_id>/", views.detalle_lugar, name="detalle"),
    path("lugar/<int:lugar_id>/favorito/", views.cambiar_favorito, name="cambiar_favorito"),
    path("favoritos/", views.mis_favoritos, name="favoritos"),
    path("cerca/", views.cerca_de_ti, name="cerca"),
    path("api/lugares/", views.api_lugares, name="api_lugares"),
    path("sw.js", views.service_worker, name="service_worker"),
]
