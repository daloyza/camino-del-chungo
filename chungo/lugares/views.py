from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import Lugar

# Distancia máxima (en metros) para que un lugar cuente como "cerca".
# Es el único lugar donde está este número: si lo cambias aquí, cambia en toda la app.
RADIO_METROS = 50


def lista_lugares(request):
    lugares = Lugar.objects.all()
    return render(request, "lugares/lista.html", {"lugares": lugares})


def detalle_lugar(request, lugar_id):
    lugar = get_object_or_404(Lugar, id=lugar_id)
    return render(request, "lugares/detalle.html", {"lugar": lugar})


def cerca_de_ti(request):
    return render(request, "lugares/cerca.html", {"radio_metros": RADIO_METROS})


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
