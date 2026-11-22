"""Importa los Monumentos Nacionales de Santiago Centro desde la API de IDE Patrimonio.

Uso (dentro de la carpeta chungo):
    python manage.py importar_patrimonio

Fuente: IDE Patrimonio, Subsecretaría del Patrimonio Cultural (ide.patrimoniocultural.gob.cl),
capa "Puntos de Monumentos Nacionales" del Consejo de Monumentos Nacionales.

Se puede correr las veces que se quiera: actualiza los lugares que ya existen en vez de duplicarlos.
Los 9 lugares escritos por el equipo no se tocan (solo se les actualizan las coordenadas oficiales).
Solo se guardan los monumentos que tienen foto y que están en Santiago Centro o sus alrededores
(a RADIO_CENTRO_METROS o menos de la Plaza de Armas).
La descripción para turistas se arma en lugares/descripciones_turisticas.py.
"""

import json
import re
import unicodedata
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from math import asin, cos, radians, sin, sqrt

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError

from lugares.descripciones_turisticas import descripcion_turistica
from lugares.models import Lugar

URL_API = (
    "https://idepat.patrimoniocultural.gob.cl/server/rest/services/"
    "ProducciónPatrimonio/Puntos_Monumentos_Nacionales/FeatureServer/0/query"
)
COMUNA = "Santiago"  # la comuna de Santiago es Santiago Centro
CAMPOS = "codigo,nombre,categoria,lat,long,imagen,fch_dec"
AGENTE = "camino-del-chungo/1.0 (proyecto universitario)"
ESPERA_SEGUNDOS = 30
DISTANCIA_REPETIDOS = 200  # metros: partes de un mismo monumento a esta distancia se juntan

# Santiago Centro y alrededores: lugares a esta distancia o menos de la Plaza de Armas
PLAZA_DE_ARMAS = (-33.4378, -70.6504)
RADIO_CENTRO_METROS = 2000


def pedir(url):
    solicitud = urllib.request.Request(url, headers={"User-Agent": AGENTE})
    with urllib.request.urlopen(solicitud, timeout=ESPERA_SEGUNDOS) as respuesta:
        return respuesta.read()


def descargar_monumentos():
    """Pide a la API todos los monumentos de la comuna (de a páginas si son muchos)."""
    monumentos = []
    desde = 0
    while True:
        parametros = urllib.parse.urlencode({
            "where": f"comuna='{COMUNA}'",
            "outFields": CAMPOS,
            "returnGeometry": "false",
            "orderByFields": "codigo",
            "resultOffset": desde,
            "f": "json",
        })
        datos = json.loads(pedir(urllib.parse.quote(URL_API, safe=":/") + "?" + parametros))
        if "error" in datos:
            raise CommandError(f"La API respondió con un error: {datos['error']}")
        pagina = [registro["attributes"] for registro in datos.get("features", [])]
        monumentos += pagina
        if not datos.get("exceededTransferLimit") or not pagina:
            return monumentos
        desde += len(pagina)


def anio_del_decreto(milisegundos):
    if milisegundos is None:
        return None
    return (datetime(1970, 1, 1, tzinfo=timezone.utc) + timedelta(milliseconds=milisegundos)).year


def armar_descripcion(monumento, idioma):
    return descripcion_turistica(
        monumento["nombre"].strip(), monumento["categoria"] or "", anio_del_decreto(monumento.get("fch_dec")), idioma
    )


def distancia_metros(lat1, lon1, lat2, lon2):
    # Fórmula de Haversine (la misma que usa la página "Cerca de ti")
    dlat, dlon = radians(lat2 - lat1), radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    return 2 * 6371000 * asin(sqrt(a))


def nombre_simple(texto):
    # Sin tildes ni mayúsculas, para comparar nombres
    sin_tildes = unicodedata.normalize("NFD", texto.strip().lower())
    return "".join(letra for letra in sin_tildes if unicodedata.category(letra) != "Mn")


def juntar_repetidos(monumentos):
    """El catálogo divide algunos monumentos en varias partes con el mismo nombre
    (por ejemplo, una iglesia y su convento). Si están cerca, se deja uno solo."""
    elegidos = []
    for monumento in monumentos:
        repetido = any(
            nombre_simple(monumento["nombre"]) == nombre_simple(otro["nombre"])
            and distancia_metros(monumento["lat"], monumento["long"], otro["lat"], otro["long"]) <= DISTANCIA_REPETIDOS
            for otro in elegidos
        )
        if not repetido:
            elegidos.append(monumento)
    return elegidos


def url_de_la_foto(monumento):
    # La API entrega la foto dentro de una etiqueta <img src="...">
    encontrado = re.search(r'src="([^"]+)"', monumento.get("imagen") or "")
    return encontrado.group(1) if encontrado else ""


class Command(BaseCommand):
    help = "Importa los Monumentos Nacionales de Santiago Centro desde IDE Patrimonio."

    def handle(self, *args, **opciones):
        self.stdout.write("Consultando IDE Patrimonio...")
        try:
            monumentos = descargar_monumentos()
        except OSError as error:
            raise CommandError(f"No se pudo conectar con IDE Patrimonio. Revisa tu internet. ({error})")
        self.stdout.write(f"La API entregó {len(monumentos)} monumentos de la comuna de {COMUNA}.")

        monumentos = [
            m for m in monumentos
            if m.get("codigo") and m.get("nombre") and m.get("lat") is not None and m.get("long") is not None
        ]
        # Los códigos de los lugares del equipo van primero, para que no se pierdan al juntar repetidos
        codigos_propios = set(Lugar.objects.filter(desde_ide=False).exclude(codigo_ide=None).values_list("codigo_ide", flat=True))
        monumentos.sort(key=lambda m: (m["codigo"] not in codigos_propios, m["codigo"]))
        monumentos = juntar_repetidos(monumentos)

        nuevos = actualizados = propios = fotos = 0
        lejos = sin_foto = 0
        codigos_guardados = []
        for monumento in monumentos:
            codigo = monumento["codigo"]
            lugar = Lugar.objects.filter(codigo_ide=codigo).first()

            # Lugar escrito por el equipo: se conserva su historia, solo se corrigen las coordenadas
            if lugar and not lugar.desde_ide:
                lugar.latitud = monumento["lat"]
                lugar.longitud = monumento["long"]
                lugar.categoria = monumento["categoria"] or ""
                lugar.save()
                propios += 1
                continue

            # Fuera de Santiago Centro y alrededores (o con coordenadas erróneas): no se guarda
            if distancia_metros(*PLAZA_DE_ARMAS, monumento["lat"], monumento["long"]) > RADIO_CENTRO_METROS:
                lejos += 1
                continue

            es_nuevo = lugar is None
            if es_nuevo:
                lugar = Lugar(codigo_ide=codigo, desde_ide=True)

            # Sin foto no se guarda: se baja solo si todavía no la tiene
            if not lugar.foto:
                url_foto = url_de_la_foto(monumento)
                try:
                    if not url_foto:
                        raise OSError("la API no trae foto")
                    lugar.foto.save(f"ide_{codigo}.jpg", ContentFile(pedir(url_foto)), save=False)
                    fotos += 1
                except OSError:
                    sin_foto += 1
                    continue

            lugar.nombre = monumento["nombre"].strip()
            lugar.categoria = monumento["categoria"] or ""
            lugar.latitud = monumento["lat"]
            lugar.longitud = monumento["long"]
            lugar.descripcion = armar_descripcion(monumento, "es")
            lugar.descripcion_en = armar_descripcion(monumento, "en")
            lugar.descripcion_pt = armar_descripcion(monumento, "pt")
            lugar.save()
            codigos_guardados.append(codigo)
            if es_nuevo:
                nuevos += 1
            else:
                actualizados += 1

        # Borra los lugares importados antes que ya no cumplen (lejos, sin foto, repetidos o fuera del catálogo)
        sobrantes = Lugar.objects.filter(desde_ide=True).exclude(codigo_ide__in=codigos_guardados)
        for lugar in sobrantes:
            if lugar.foto:
                lugar.foto.delete(save=False)  # también borra el archivo de la foto
        _, por_modelo = sobrantes.delete()
        borrados = por_modelo.get("lugares.Lugar", 0)

        self.stdout.write(self.style.SUCCESS(
            f"Listo: {nuevos} lugares nuevos, {actualizados} actualizados, {borrados} borrados "
            f"y {propios} lugares del equipo con coordenadas oficiales. Se bajaron {fotos} fotos."
        ))
        self.stdout.write(
            f"Quedaron fuera {lejos} monumentos lejos del centro y {sin_foto} sin foto. "
            f"Total de lugares en la app: {Lugar.objects.count()}."
        )
