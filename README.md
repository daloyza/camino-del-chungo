# El camino del chungo

App web hecha con Django. La persona camina y, si esta cerca de un lugar
registrado, la app le avisa que puede desbloquearlo. Al entrar ve el lugar y
puede leer la descripcion, escucharla o no leerla. Hay un ranking de la
Region Metropolitana con quien ha desbloqueado mas lugares. No lleva mapa.

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

## URLs
- /            lista de lugares (de prueba)
- /cerca/      lugares a 50 metros o menos de tu ubicacion
- /lugar/<id>/ detalle del lugar: Leer, Escuchar y No leer
- /api/lugares/ lugares en formato JSON
- /admin/      panel de administracion

## Que esta hecho
- Modelo Lugar (nombre, descripcion, foto, latitud, longitud)
- Panel de administracion para cargar lugares
- Pagina con la lista de lugares (es solo de prueba)
- Detalle del lugar con foto y botones Leer, Escuchar (voz del navegador) y No leer
- Pagina "cerca de ti": pide la ubicacion, calcula la distancia a cada lugar
  (formula de Haversine) y muestra solo los que estan a 50 metros o menos

## Que falta (en este orden)
1. Registro e inicio de sesion de usuarios
2. Guardar los lugares desbloqueados y armar el ranking
3. Notificaciones del navegador al estar cerca de un lugar
4. Revisar un lugar que quedo sin foto