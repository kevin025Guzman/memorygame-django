# memorygame-django
Proyecto clase arquitectura de computadoras - MemoryGame - Django-Python

## Descripción

Aplicación web tipo juego de memoria que permite a usuarios registrados seleccionar nivel de dificultad, jugar con tablero 4x4 cronometrado y registrar automáticamente sus resultados. El backend en Django maneja autenticación, persistencia de partidas y estadísticas (historial personal, promedios, nivel más jugado y ranking global de victorias por nivel). El frontend usa Bootstrap + JS personalizado para la lógica del juego, efectos audiovisuales y controles de accesibilidad. El proyecto incluye Dockerfile/compose para despliegue con Gunicorn y scripts que ejecutan migraciones y `collectstatic` al iniciar.

## Despliegue en Render con Docker

1. **Variables de entorno obligatorias**
   - `DJANGO_SECRET_KEY`
   - `DATABASE_URL` (Render la define automáticamente para Postgres)
   - `DJANGO_ALLOWED_HOSTS` y `DJANGO_CSRF_TRUSTED_ORIGINS` (por ejemplo `your-app.onrender.com`)

2. **Servicio Web**
   - Tipo: *Web Service*
   - Runtime: *Docker*
   - Dockerfile: raíz del proyecto (`Dockerfile`)
   - Build Command: *(vacío, Render usa el Dockerfile)*
   - Start Command: *(vacío, el Dockerfile ya ejecuta `render-entrypoint.sh`)*

3. **Proceso de despliegue**
   - Render construye la imagen usando el Dockerfile.
   - El script `render-entrypoint.sh` aplica migraciones, recolecta estáticos y arranca Gunicorn.

4. **Archivos estáticos**
   - `collectstatic` guarda los archivos en `staticfiles/` y WhiteNoise los sirve desde la misma app, por lo que no se requiere almacenamiento externo.

5. **Migraciones**
   - Se ejecutan automáticamente en cada despliegue gracias al script de entrada.



!!!IMPORTANTE!!!
Debido a que el servidor está en la capa gratuita tiene un pequeño shutdown por inactividad así que al ingresar al sitio se debe esperar a que cargue el servicio.
