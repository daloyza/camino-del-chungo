from django.urls import path
from . import views

urlpatterns = [
    path("", views.lista_lugares, name="lista"),
]
urlpatterns = [
    path("", views.lista_lugares, name="lista"),
    path("lugar/<int:lugar_id>/", views.detalle_lugar, name="detalle"),
]