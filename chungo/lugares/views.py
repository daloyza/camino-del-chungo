from django.shortcuts import render, get_object_or_404

from .models import Lugar

def lista_lugares(request):
    lugares = Lugar.objects.all()
    return render(request, "lugares/lista.html", {"lugares": lugares})

def detalle_lugar(request, lugar_id):
    lugar = get_object_or_404(Lugar, id=lugar_id)
    return render(request, "lugares/detalle.html", {"lugar": lugar})
# Create your views here.
