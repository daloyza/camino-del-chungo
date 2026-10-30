from django.urls import path
from . import views

urlpatterns = [
    path("", views.lista_lugares, name="lista"),
    path("lugar/<int:lugar_id>/", views.detalle_lugar, name="detalle"),
    path("cerca/", views.cerca_de_ti, name="cerca"),
    path("api/lugares/", views.api_lugares, name="api_lugares"),
]
