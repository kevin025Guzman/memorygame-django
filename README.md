# memorygame-django
Proyecto clase arquitectura de computadoras - MemoryGame - Django-Python

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
