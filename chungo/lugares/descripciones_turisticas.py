"""Descripciones para turistas de los lugares que vienen de IDE Patrimonio.

La API no trae la historia de cada monumento, así que el texto se arma según el
tipo de lugar (iglesia, palacio, teatro, etc.), que se reconoce por su nombre.
Si un lugar necesita un texto propio, se puede escribir en /admin/ y desmarcar
"importado desde IDE Patrimonio" para que la importación no lo cambie.
"""

import unicodedata


def simple(texto):
    sin_tildes = unicodedata.normalize("NFD", texto.lower())
    return "".join(letra for letra in sin_tildes if unicodedata.category(letra) != "Mn")


# Tipos de lugar: palabras que lo identifican en el nombre (sin tildes) y textos por idioma.
# Se revisan en orden: el primero que coincide es el que se usa.
TIPOS = [
    {
        "palabras": ["memoria", "detencion", "victor jara", "fasic"],
        "es": ("Es un sitio de memoria, protegido para recordar hechos importantes de la historia reciente de Chile y a las personas que los vivieron.",
               "Recomendación: visítalo con respeto. Algunos sitios de memoria ofrecen visitas guiadas; revisa sus horarios antes de ir."),
        "en": ("It is a memory site, protected to remember important events in Chile's recent history and the people who lived through them.",
               "Tip: visit it with respect. Some memory sites offer guided tours, so check their opening hours before you go."),
        "pt": ("É um lugar de memória, protegido para lembrar fatos importantes da história recente do Chile e as pessoas que os viveram.",
               "Dica: visite com respeito. Alguns lugares de memória oferecem visitas guiadas; confira os horários antes de ir."),
    },
    {
        "palabras": ["iglesia", "basilica", "templo", "convento", "sagrario"],
        "es": ("Forma parte del patrimonio religioso de la ciudad, levantado a lo largo de varios siglos. Estas iglesias suelen guardar altares, imágenes y detalles artísticos que vale la pena mirar con calma.",
               "Recomendación: si está abierta, entra en silencio y respeta los horarios de misa. Fíjate en la fachada, el techo y los altares."),
        "en": ("It is part of the city's religious heritage, built over several centuries. Churches like this one often keep altars, statues and artistic details worth taking your time to look at.",
               "Tip: if it is open, go in quietly and respect mass times. Take a look at the façade, the ceiling and the altars."),
        "pt": ("Faz parte do patrimônio religioso da cidade, construído ao longo de vários séculos. Essas igrejas costumam guardar altares, imagens e detalhes artísticos que valem a pena observar com calma.",
               "Dica: se estiver aberta, entre em silêncio e respeite os horários de missa. Repare na fachada, no teto e nos altares."),
    },
    {
        "palabras": ["teatro"],
        "es": ("Los teatros como este fueron puntos de encuentro de la vida cultural y social de Santiago, donde varias generaciones se reunieron a ver espectáculos.",
               "Recomendación: mira su fachada y revisa si tiene funciones o actividades abiertas al público durante tu visita."),
        "en": ("Theaters like this one were meeting points for Santiago's cultural and social life, where several generations gathered to enjoy shows.",
               "Tip: take a look at its façade and check whether it has shows or activities open to the public during your visit."),
        "pt": ("Teatros como este foram pontos de encontro da vida cultural e social de Santiago, onde várias gerações se reuniram para assistir a espetáculos.",
               "Dica: observe a fachada e veja se há apresentações ou atividades abertas ao público durante a sua visita."),
    },
    {
        "palabras": ["mural"],
        "es": ("Es una obra de arte pública que se puede ver gratis, como parte del recorrido diario de quienes viven en la ciudad.",
               "Recomendación: tómate un momento para mirarlo de cerca y descubrir sus colores y detalles. Es un buen lugar para sacar fotos."),
        "en": ("It is a public work of art that you can see for free, as part of the daily routine of the people who live in the city.",
               "Tip: take a moment to look at it up close and discover its colors and details. It is a great spot for photos."),
        "pt": ("É uma obra de arte pública que pode ser vista de graça, como parte do caminho diário de quem vive na cidade.",
               "Dica: reserve um momento para observá-lo de perto e descobrir suas cores e detalhes. É um ótimo lugar para tirar fotos."),
    },
    {
        "palabras": ["puente", "calzada"],
        "es": ("Es parte de la historia de cómo Santiago fue construyendo sus puentes y calles para conectar sus barrios a medida que la ciudad crecía.",
               "Recomendación: recórrelo a pie, con calma, y aprovecha de caminar por los alrededores."),
        "en": ("It is part of the story of how Santiago built its bridges and streets to connect its neighborhoods as the city grew.",
               "Tip: explore it on foot, at a relaxed pace, and take the chance to walk around the area."),
        "pt": ("Faz parte da história de como Santiago construiu suas pontes e ruas para ligar seus bairros à medida que a cidade crescia.",
               "Dica: percorra-o a pé, com calma, e aproveite para caminhar pelos arredores."),
    },
    {
        "palabras": ["parque", "invernadero", "plazoleta"],
        "es": ("Es un espacio abierto de la ciudad, ideal para descansar un rato entre una visita y otra.",
               "Recomendación: ve de día, lleva agua y aprovecha de sentarte a disfrutar del lugar."),
        "en": ("It is an open space in the city, ideal for taking a break between one visit and the next.",
               "Tip: go during the day, bring water and take the chance to sit down and enjoy the place."),
        "pt": ("É um espaço aberto da cidade, ideal para descansar um pouco entre uma visita e outra.",
               "Dica: vá durante o dia, leve água e aproveite para se sentar e curtir o lugar."),
    },
    {
        "palabras": ["biblioteca", "archivo", "museo", "universidad", "escuela", "internado"],
        "es": ("Es un lugar ligado a la educación, el conocimiento o la cultura, y su edificio es parte importante de la historia de la ciudad.",
               "Recomendación: algunos de estos edificios se pueden visitar por dentro; revisa sus horarios. Si no, vale la pena detenerse a mirar su fachada."),
        "en": ("It is a place linked to education, knowledge or culture, and its building is an important part of the city's history.",
               "Tip: some of these buildings can be visited inside, so check their opening hours. If not, it is worth stopping to look at the façade."),
        "pt": ("É um lugar ligado à educação, ao conhecimento ou à cultura, e seu edifício é parte importante da história da cidade.",
               "Dica: alguns desses edifícios podem ser visitados por dentro; confira os horários. Se não, vale a pena parar para observar a fachada."),
    },
    {
        "palabras": ["palacio", "casa", "posada", "club de", "hotel"],
        "es": ("Es parte de la arquitectura histórica de Santiago: casas, palacios y edificios que muestran cómo se vivía y se construía en la ciudad en otras épocas.",
               "Recomendación: mira con atención su fachada, sus ventanas y sus puertas. Algunos se pueden visitar por dentro; revisa si está abierto al público."),
        "en": ("It is part of Santiago's historic architecture: houses, palaces and buildings that show how people lived and built in the city in other times.",
               "Tip: take a close look at its façade, windows and doors. Some can be visited inside, so check whether it is open to the public."),
        "pt": ("Faz parte da arquitetura histórica de Santiago: casas, palácios e edifícios que mostram como se vivia e se construía na cidade em outras épocas.",
               "Dica: observe com atenção a fachada, as janelas e as portas. Alguns podem ser visitados por dentro; veja se está aberto ao público."),
    },
]

TIPO_PARQUE = next(tipo for tipo in TIPOS if "parque" in tipo["palabras"])

# Edificios que no calzan en ningún tipo (edificios públicos, bancos, hospitales, etc.)
TIPO_EDIFICIO = {
    "es": ("Es uno de los edificios que cuentan la historia de Santiago, y destaca tanto por su arquitectura como por el papel que ha tenido en la vida de la ciudad.",
           "Recomendación: obsérvalo desde la vereda y fíjate en los detalles de su fachada. Muchos de estos edificios siguen en uso, así que no siempre se pueden visitar por dentro."),
    "en": ("It is one of the buildings that tell the story of Santiago, standing out both for its architecture and for the role it has played in the life of the city.",
           "Tip: admire it from the sidewalk and notice the details of its façade. Many of these buildings are still in use, so they cannot always be visited inside."),
    "pt": ("É um dos edifícios que contam a história de Santiago e se destaca tanto pela arquitetura quanto pelo papel que teve na vida da cidade.",
           "Dica: observe-o da calçada e repare nos detalhes da fachada. Muitos desses edifícios ainda estão em uso, por isso nem sempre podem ser visitados por dentro."),
}

# Barrios y sectores (categoría Zona Típica o Pintoresca)
TIPO_ZONA = {
    "es": ("Al caminar por sus calles se pueden ver casas, fachadas y espacios que conservan el estilo de otras épocas y le dan una identidad propia.",
           "Recomendación: recórrelo a pie, sin apuro, y aprovecha de descubrir sus calles y rincones. Es un buen lugar para sacar fotos."),
    "en": ("Walking through its streets you can see houses, façades and spaces that keep the style of other times and give it its own identity.",
           "Tip: explore it on foot, without hurrying, and take the chance to discover its streets and hidden corners. It is a great spot for photos."),
    "pt": ("Ao caminhar por suas ruas, é possível ver casas, fachadas e espaços que conservam o estilo de outras épocas e lhe dão uma identidade própria.",
           "Dica: percorra-o a pé, sem pressa, e aproveite para descobrir suas ruas e cantinhos. É um ótimo lugar para tirar fotos."),
}

# El nombre ya aparece como título en la página, por eso el texto empieza con "Este lugar"
INTRO = {
    "Zona Típica o Pintoresca": {
        "es": "Este sector es una Zona Típica de Santiago Centro, protegida por ley{desde} para conservar su ambiente y su arquitectura.",
        "en": "This area is a Typical Zone in downtown Santiago, protected by law{desde} to preserve its atmosphere and architecture.",
        "pt": "Este setor é uma Zona Típica do centro de Santiago, protegida por lei{desde} para conservar seu ambiente e sua arquitetura.",
    },
    "Monumento Histórico": {
        "es": "Este lugar es uno de los Monumentos Históricos de Santiago Centro, con protección legal{desde}.",
        "en": "This place is one of the Historic Monuments of downtown Santiago, legally protected{desde}.",
        "pt": "Este lugar é um dos Monumentos Históricos do centro de Santiago, com proteção legal{desde}.",
    },
}
INTRO_GENERAL = {
    "es": "Este lugar es un Monumento Nacional de Santiago Centro, con protección legal{desde}.",
    "en": "This place is a National Monument in downtown Santiago, legally protected{desde}.",
    "pt": "Este lugar é um Monumento Nacional do centro de Santiago, com proteção legal{desde}.",
}
DESDE = {"es": " desde {anio}", "en": " since {anio}", "pt": " desde {anio}"}


def tipo_del_lugar(nombre, categoria):
    nombre = simple(nombre)
    if categoria == "Zona Típica o Pintoresca":
        # Un parque declarado Zona Típica se describe como parque, no como barrio
        return TIPO_PARQUE if nombre.startswith("parque") else TIPO_ZONA
    for tipo in TIPOS:
        if any(palabra in nombre for palabra in tipo["palabras"]):
            return tipo
    return TIPO_EDIFICIO


def descripcion_turistica(nombre, categoria, anio, idioma):
    """Texto breve para turistas: qué es el lugar, contexto y una recomendación."""
    desde = DESDE[idioma].format(anio=anio) if anio else ""
    intro = INTRO.get(categoria, INTRO_GENERAL)[idioma].format(desde=desde)
    contexto, recomendacion = tipo_del_lugar(nombre, categoria)[idioma]
    return f"{intro} {contexto}\n\n{recomendacion}"
