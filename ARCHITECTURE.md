# Arquitectura

## Vista general

```text
Next.js Frontend
    |
    | HTTP + JWT
    v
FastAPI Backend
    |-- PostgreSQL: usuarios, metadata, estados y OCR text
    |-- MinIO: archivos originales
    |
    | Redis broker
    v
Celery Worker
    |
    v
OCR Processor mock
```

## Flujo de upload

1. El frontend envia `POST /documents` con JWT y archivo multipart.
2. FastAPI valida extension, content type, tamano y usuario autenticado.
3. El archivo se guarda en MinIO usando un `object_name` unico por usuario.
4. La metadata se guarda en PostgreSQL con estado `uploaded`.
5. Se encola `process_document_ocr(document_id)` en Redis.
6. La API responde `document_id` y estado inicial.

## Flujo de OCR

1. Celery toma el job.
2. El worker busca el documento en PostgreSQL.
3. Cambia estado a `processing`.
4. Descarga el archivo desde MinIO.
5. Ejecuta OCR mock controlado.
6. Guarda `ocr_text`, `processed_at` y estado `completed`.
7. Si ocurre un error, guarda `error_message` y estado `failed`.

## Decisiones tecnicas

- **JWT**: mecanismo simple y suficiente para autenticar API y frontend.
- **PostgreSQL**: persistencia relacional para usuarios, ownership y estados.
- **MinIO**: separa archivos binarios de la base de datos y simula storage tipo S3.
- **Redis + Celery**: procesamiento asincrono real sin bloquear requests HTTP.
- **Polling**: suficiente para el reto, simple de implementar y facil de defender.
- **OCR mock**: prioriza flujo end-to-end estable. OCR real queda como mejora sin comprometer la entrega base.

## Seguridad y ownership

Todas las consultas de documentos filtran por `document.id` y `document.user_id`. Si un documento no pertenece al usuario autenticado, la API responde `404` para no revelar su existencia.
