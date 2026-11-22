# El camino del chungo

App web hecha con Django. La persona camina y, si esta cerca de un lugar
registrado, la app le avisa que puede desbloquearlo. Al entrar ve el lugar y
puede leer la descripcion, escucharla o no leerla, y guardarlo en sus
favoritos. No pide crear cuenta y no lleva mapa.

Funcionalidades:
- Corazon: aviso por cercania (50 m) y vista rapida de la historia del lugar.
- Funcionalidad 2: reproductor multimodal (Leer o Escuchar, con pausa).
- Funcionalidad 3: coleccion de favoritos guardada en la base de datos.

## Como encenderlo (Windows)

1. Abrir la carpeta en VS Code y abrir una terminal.
2. Crear y activar el entorno virtual:
     python -m venv entorno_proyecto
     entorno_proyecto\Scripts\activate
3. Instalar lo necesario:
     pip install -r requirements.txt
4. Entrar a la carpeta chungo y preparar la base de datos:
     cd chungo
     python manage.py migrate
     python manage.py loaddata datos_lugares.json
     python manage.py importar_patrimonio
     python manage.py createsuperuser
5. Encender el servidor:
     python manage.py runserver
6. Pagina: http://127.0.0.1:8000/   Panel: http://127.0.0.1:8000/admin

## Como probar la funcionalidad corazon ("cerca de ti")

1. Abrir http://127.0.0.1:8000/cerca/ en Chrome.
2. Simular la ubicacion: F12 > menu de tres puntos > More tools > Sensors >
   Location > Other... y escribir las coordenadas.
3. Tocar "Buscar lugares cerca de mi" y permitir la ubicacion.

Datos de prueba:
- Caso 1 (cerca): latitud -33.439327, longitud -70.643381 (Cerro Santa Lucia).
  Debe aparecer "Cerro Santa Lucia" a 0 metros con el boton "Desbloquear".
- Caso 2 (lejos): latitud -33.4347, longitud -70.6560.
  Debe decir que no hay lugares a menos de 50 metros y que el mas cercano es
  Hotel Bristol, a unos 302 metros.

El radio de 50 metros se cambia en chungo/lugares/views.py (RADIO_METROS).

## Avisos al estar cerca de un lugar

1. En /cerca/ tocar "Activar avisos" y elegir "Permitir".
2. Simular la ubicacion del Caso 1: aparece un aviso del sistema
   "Estas cerca de Cerro Santa Lucia". Al tocarlo se abre el lugar.
3. Si no se dan permisos, aparece un aviso azul dentro de la pagina.
4. El aviso de un mismo lugar no se repite antes de 6 horas. Para volver a
   probarlo: F12 > Application > Local Storage > borrar "chungo_avisados".

Limitaciones:
- Solo funciona con la pagina /cerca/ abierta (no avisa con el navegador cerrado).
- En iPhone solo funciona si la web esta agregada a la pantalla de inicio.
- El celular necesita HTTPS: con http://192.168.x.x no hay ubicacion ni avisos.
  En el computador funciona porque 127.0.0.1 cuenta como seguro.

## Favoritos (persistencia de datos)

1. Abrir un lugar, por ejemplo http://127.0.0.1:8000/lugar/1/
2. Tocar "Guardar en favoritos": el boton cambia a "Quitar de favoritos".
3. Abrir http://127.0.0.1:8000/favoritos/ : aparece el lugar con su fecha.
4. Evidencia en la base de datos: http://127.0.0.1:8000/admin/ > Favoritos.
   Cada fila tiene el lugar, el codigo del visitante y la fecha.

No hay cuentas: cada navegador recibe un codigo al azar que se guarda en la
sesion (cookie de un ano). Otro navegador o una ventana de incognito tiene
su propia lista. Si se borran las cookies, se pierde la lista.

Modelo de datos: Lugar (1) --- (N) Favorito
- Lugar: nombre, descripcion, foto, latitud, longitud, sus traducciones y
  los datos de IDE Patrimonio (codigo_ide, categoria, desde_ide)
- Favorito: visitante, lugar (llave foranea a Lugar), fecha
  Un visitante no puede guardar dos veces el mismo lugar.

## Datos de IDE Patrimonio (API)

Los lugares de Santiago Centro vienen de la API de IDE Patrimonio, la
Infraestructura de Datos Espaciales de la Subsecretaria del Patrimonio
Cultural (https://ide.patrimoniocultural.gob.cl). Se usa la capa "Puntos de
Monumentos Nacionales" del Consejo de Monumentos Nacionales, filtrada por la
comuna de Santiago (Santiago Centro): Monumentos Historicos y Zonas Tipicas.

Para traer los datos (necesita internet), dentro de la carpeta chungo:

    python manage.py importar_patrimonio

- Trae nombre, categoria, coordenadas oficiales y foto de cada monumento.
- La API no trae la historia de cada lugar, asi que se arma una descripcion
  breve para turistas segun el tipo de lugar (iglesia, palacio, teatro,
  sitio de memoria, barrio, etc.), con una recomendacion, en espanol, ingles
  y portugues. Los textos estan en chungo/lugares/descripciones_turisticas.py
- Para escribir un texto propio de un lugar: editarlo en /admin/ y desmarcar
  "importado desde IDE Patrimonio", asi la importacion no lo cambia.
- Se puede correr las veces que se quiera: actualiza sin duplicar.
- Los 9 lugares escritos por el equipo (datos_lugares.json) conservan su
  historia y su foto; solo se les ponen las coordenadas oficiales.
- Solo se guardan los monumentos que tienen foto y que estan en Santiago
  Centro o sus alrededores: a 2 km o menos de la Plaza de Armas
  (RADIO_CENTRO_METROS en el comando).
- La app funciona sin internet despues de importar: todo queda en la base
  de datos y las fotos en chungo/media/lugares/.
- El codigo esta en chungo/lugares/management/commands/importar_patrimonio.py

## Idiomas (espanol, ingles y portugues)

Arriba a la derecha estan los botones ES / EN / PT. El idioma elegido se
guarda en la sesion y cambia los textos de la app, el nombre y la historia
de cada lugar, los avisos y la voz de "Escuchar".

- Textos de la app: chungo/lugares/idiomas.py
- Nombre e historia traducidos: campos nombre_en, descripcion_en, nombre_pt
  y descripcion_pt del modelo Lugar (se editan en /admin/). Si estan vacios
  se muestra el texto en espanol.

Despues de bajar este cambio hay que correr, dentro de la carpeta chungo:

    python manage.py migrate
    python manage.py loaddata datos_lugares.json

## URLs
- /            lista de lugares
- /cerca/      lugares a 50 metros o menos de tu ubicacion
- /lugar/<id>/ detalle del lugar: Leer, Escuchar, No leer y favoritos
- /favoritos/  lugares guardados por este navegador
- /api/lugares/ lugares en formato JSON
- /idioma/<es|en|pt>/ cambia el idioma
- /sw.js       Service Worker de los avisos
- /admin/      panel de administracion

## Que esta hecho
- Modelo Lugar (nombre, descripcion, foto, latitud, longitud)
- Panel de administracion para cargar lugares
- Pagina con la lista de lugares
- Detalle del lugar con foto y botones Leer, Escuchar (voz del navegador) y No leer
- Recuadro de reemplazo cuando un lugar no tiene foto
- Pagina "cerca de ti": pide la ubicacion, calcula la distancia a cada lugar
  (formula de Haversine) y muestra solo los que estan a 50 metros o menos
- Avisos del navegador al llegar a un lugar (con aviso dentro de la pagina
  como respaldo)
- Coleccion de favoritos guardada en la base de datos (modelo Favorito)
- Traduccion al ingles y al portugues (selector ES / EN / PT)
- Lugares de Santiago Centro importados desde la API de IDE Patrimonio
