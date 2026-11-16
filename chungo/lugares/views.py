import uuid

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .idiomas import IDIOMAS, TEXTOS, idioma_de
from .models import Favorito, Lugar

# Radio (metros) para considerar que un lugar está cerca. Lo usan /cerca/ y la API.
RADIO_METROS = 50


def codigo_visitante(request):
    # Identifica al navegador sin pedir cuenta: se guarda en la sesión (cookie)
    if "visitante" not in request.session:
        request.session["visitante"] = uuid.uuid4().hex
    return request.session["visitante"]


def cambiar_idioma(request, codigo):
    # Guarda el idioma elegido y vuelve a la página donde estaba la persona
    if codigo in IDIOMAS:
        request.session["idioma"] = codigo
    volver_a = request.GET.get("next", "")
    if not url_has_allowed_host_and_scheme(volver_a, allowed_hosts={request.get_host()}):
        volver_a = reverse("lista")
    return redirect(volver_a)


def lista_lugares(request):
    idioma = idioma_de(request)
    lugares = [lugar.traducir(idioma) for lugar in Lugar.objects.all()]
    return render(request, "lugares/lista.html", {"lugares": lugares})


def detalle_lugar(request, lugar_id):
    lugar = get_object_or_404(Lugar, id=lugar_id).traducir(idioma_de(request))
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
    idioma = idioma_de(request)
    favoritos = list(Favorito.objects.filter(visitante=codigo_visitante(request)).select_related("lugar"))
    for favorito in favoritos:
        favorito.lugar.traducir(idioma)
    return render(request, "lugares/favoritos.html", {"favoritos": favoritos})


def cerca_de_ti(request):
    intro = TEXTOS[idioma_de(request)]["cerca_intro"].format(radio=RADIO_METROS)
    return render(request, "lugares/cerca.html", {"radio_metros": RADIO_METROS, "intro": intro})


def service_worker(request):
    # Va en la raíz (/sw.js) para que su alcance cubra toda la app
    return render(request, "lugares/sw.js", content_type="application/javascript")


def api_lugares(request):
    idioma = idioma_de(request)
    datos = []
    for lugar in Lugar.objects.all():
        lugar.traducir(idioma)
        datos.append({
            "id": lugar.id,
            "nombre": lugar.nombre_mostrado,
            "latitud": lugar.latitud,
            "longitud": lugar.longitud,
            "foto": lugar.foto.url if lugar.foto else "",
            "url": reverse("detalle", args=[lugar.id]),
        })
    return JsonResponse({"radio_metros": RADIO_METROS, "idioma": idioma, "lugares": datos})
