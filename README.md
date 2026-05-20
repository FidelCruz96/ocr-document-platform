# OCR Document Platform

Plataforma pequena para iniciar sesion, subir documentos, procesarlos en background con OCR mock controlado y visualizar el texto extraido desde una UI web.

## Stack

- Backend: FastAPI, SQLAlchemy, PostgreSQL.
- Worker: Celery con Redis.
- Storage: MinIO.
- Frontend: Next.js.
- Contenedores: Docker Compose.

## Como ejecutar

```bash
docker compose up --build
```

Servicios locales:

- Frontend: http://localhost:3000
- Backend docs: http://localhost:8000/docs
- MinIO console: http://localhost:9001

Credenciales demo:

- App: `admin@test.com` / `admin123`
- MinIO: `minioadmin` / `minioadmin`

## Flujo funcional

1. El usuario inicia sesion y recibe un JWT.
2. El usuario sube un archivo JPG, PNG o PDF de hasta 10 MB.
3. El backend valida el archivo, lo guarda en MinIO y persiste metadata en PostgreSQL.
4. El backend encola un job Celery en Redis.
5. El worker descarga el archivo, ejecuta OCR mock reemplazable y actualiza el estado.
6. El frontend consulta el estado con polling cada 2.5 segundos hasta `completed` o `failed`.

## Endpoints principales

- `GET /health`
- `POST /auth/login`
- `GET /auth/me`
- `POST /documents`
- `GET /documents`
- `GET /documents/{id}`
- `GET /documents/{id}/status`
- `GET /documents/{id}/ocr`
- `DELETE /documents/{id}`

Los endpoints de documentos requieren `Authorization: Bearer <token>`.

## Variables de entorno relevantes

- `DATABASE_URL`
- `REDIS_URL`
- `MINIO_ENDPOINT`
- `MINIO_ACCESS_KEY`
- `MINIO_SECRET_KEY`
- `MINIO_BUCKET`
- `SECRET_KEY`
- `CORS_ORIGINS`
- `NEXT_PUBLIC_API_BASE_URL`

Los valores locales de desarrollo estan definidos en `docker-compose.yml`. No usar esos valores en produccion.

## Limitaciones

- El OCR es mock controlado para asegurar el flujo completo del reto.
- El worker tiene idempotencia basica para no reprocesar documentos completados y retries simples para errores temporales.
- No hay registro de usuarios; se crea un usuario seed local.
- No se incluyen migraciones Alembic en v1; el backend crea tablas al iniciar para simplificar la demo.
- Las decisiones tecnicas principales estan documentadas en `DECISIONS.md`.

## Mejoras futuras

- OCR real con Tesseract, EasyOCR o servicio externo.
- Migraciones con Alembic.
- Tests de integracion con PostgreSQL, Redis y MinIO.
- CI con build y tests.
- Registro de usuarios y gestion de contrasenas.
