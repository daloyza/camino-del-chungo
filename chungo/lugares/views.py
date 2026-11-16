import uuid

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST

from .models import Favorito, Lugar

# Radio (metros) para considerar que un lugar está cerca. Lo usan /cerca/ y la API.
RADIO_METROS = 50


def codigo_visitante(request):
    # Identifica al navegador sin pedir cuenta: se guarda en la sesión (cookie)
    if "visitante" not in request.session:
        request.session["visitante"] = uuid.uuid4().hex
    return request.session["visitante"]


def lista_lugares(request):
    lugares = Lugar.objects.all()
    return render(request, "lugares/lista.html", {"lugares": lugares})


def detalle_lugar(request, lugar_id):
    lugar = get_object_or_404(Lugar, id=lugar_id)
    es_favorito = Favorito.objects.filter(visitante=codigo_visitante(request), lugar=lugar).exists()
    return render(request, "lugares/detalle.html", {"lugar": lugar, "es_favorito": es_favorito})


@require_POST
def cambiar_favorito(request, lugar_id):
    lugar = get_object_or_404(Lugar, id=lugar_id)
    favorito, creado = Favorito.objects.get_or_create(visitante=codigo_visitante(request), lugar=lugar)
    if not creado:
        favorito.delete()
    return redirect("detalle", lugar_id=lugar.id)


def mis_favoritos(request):
    favoritos = Favorito.objects.filter(visitante=codigo_visitante(request)).select_related("lugar")
    return render(request, "lugares/favoritos.html", {"favoritos": favoritos})


def cerca_de_ti(request):
    return render(request, "lugares/cerca.html", {"radio_metros": RADIO_METROS})


def service_worker(request):
    # Va en la raíz (/sw.js) para que su alcance cubra toda la app
    return render(request, "lugares/sw.js", content_type="application/javascript")


def api_lugares(request):
    datos = []
    for lugar in Lugar.objects.all():
        datos.append({
            "id": lugar.id,
            "nombre": lugar.nombre,
            "latitud": lugar.latitud,
            "longitud": lugar.longitud,
            "foto": lugar.foto.url if lugar.foto else "",
            "url": reverse("detalle", args=[lugar.id]),
        })
    return JsonResponse({"radio_metros": RADIO_METROS, "lugares": datos})
