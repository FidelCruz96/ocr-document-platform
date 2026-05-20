# API Design

Base URL local: `http://localhost:8000`

## Auth

| Metodo | Endpoint | Auth | Descripcion |
| --- | --- | --- | --- |
| `POST` | `/auth/login` | No | Valida email/password y devuelve JWT. |
| `GET` | `/auth/me` | Si | Devuelve el usuario autenticado. |

### `POST /auth/login`

Request:

```json
{
  "email": "admin@test.com",
  "password": "admin123"
}
```

Response:

```json
{
  "access_token": "<jwt>",
  "token_type": "bearer"
}
```

## Documents

| Metodo | Endpoint | Auth | Descripcion |
| --- | --- | --- | --- |
| `POST` | `/documents` | Si | Sube JPG, PNG o PDF y encola OCR. |
| `GET` | `/documents` | Si | Lista documentos del usuario autenticado. |
| `GET` | `/documents/{id}` | Si | Devuelve metadata de un documento propio. |
| `GET` | `/documents/{id}/status` | Si | Devuelve estado y error si existe. |
| `GET` | `/documents/{id}/ocr` | Si | Devuelve texto OCR y estado. |
| `DELETE` | `/documents/{id}` | Si | Elimina metadata y archivo de MinIO. |

### Estados

- `uploaded`
- `processing`
- `completed`
- `failed`

### `POST /documents`

Request:

- `multipart/form-data`
- Campo: `file`
- Tipos permitidos: `image/jpeg`, `image/png`, `application/pdf`
- Tamano maximo: 10 MB

Response:

```json
{
  "id": 1,
  "status": "uploaded"
}
```

### Documento

```json
{
  "id": 1,
  "original_filename": "sample.pdf",
  "content_type": "application/pdf",
  "size_bytes": 12000,
  "status": "completed",
  "error_message": null,
  "created_at": "2026-05-19T22:00:00Z",
  "updated_at": "2026-05-19T22:00:05Z",
  "processed_at": "2026-05-19T22:00:05Z"
}
```

### OCR result

```json
{
  "id": 1,
  "status": "completed",
  "ocr_text": "Mock OCR result: extracted text from uploaded document.",
  "error_message": null
}
```

## Errores esperados

- `400`: extension o content type invalido.
- `401`: token ausente, invalido o expirado.
- `404`: documento inexistente o no perteneciente al usuario.
- `413`: archivo mayor al limite permitido.
