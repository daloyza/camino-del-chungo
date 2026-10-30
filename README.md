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

## Que esta hecho
- Modelo Lugar (nombre, descripcion, foto, latitud, longitud)
- Panel de administracion para cargar lugares
- Pagina con la lista de lugares (es solo de prueba)
- Vista y URL de detalle de un lugar (falta su plantilla detalle.html)

## Que falta (en este orden)
1. Plantilla lugares/detalle.html: foto, descripcion y botones Leer, Escuchar y No leer
2. Pagina "cerca de ti": pedir la ubicacion al navegador, calcular la distancia
   a cada lugar y mostrar solo los que estan a unos 50 metros
3. Registro e inicio de sesion de usuarios
4. Guardar los lugares desbloqueados y armar el ranking
5. Notificaciones del navegador al estar cerca de un lugar
6. Revisar un lugar que quedo sin foto