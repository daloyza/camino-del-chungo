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
- Caso 1 (cerca): latitud -33.440259, longitud -70.653633 (Cerro Santa Lucia).
  Debe aparecer "Cerro Santa Lucia" a 0 metros con el boton "Desbloquear".
- Caso 2 (lejos): latitud -33.4450, longitud -70.6600.
  Debe decir que no hay lugares a menos de 50 metros y que el mas cercano es
  Palacio de La Moneda, a unos 612 metros.

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
- Lugar: nombre, descripcion, foto, latitud, longitud y sus traducciones
- Favorito: visitante, lugar (llave foranea a Lugar), fecha
  Un visitante no puede guardar dos veces el mismo lugar.

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
