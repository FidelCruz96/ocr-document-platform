# Technical Decisions

This document captures the main implementation tradeoffs for the OCR Document Platform.

## Celery + Redis

Document OCR runs outside the HTTP request cycle. Celery with Redis keeps uploads responsive and gives a clear place to add retries, monitoring and worker scaling later.

## MinIO

Original files are stored outside PostgreSQL because they are binary objects. MinIO provides an S3-like API locally, which makes the storage layer close to a production object-storage setup without requiring cloud infrastructure.

## Polling Instead Of WebSockets

The frontend uses polling every 2.5 seconds while a document is `uploaded` or `processing`. This is simple, reliable for the expected workload, and enough for a technical challenge. WebSockets or Server-Sent Events would be reasonable if the app needed near real-time updates at higher scale.

## Mock OCR

The MVP uses a controlled mock OCR provider. The goal is to prove the complete flow: upload, persistence, queueing, background processing, state transitions and UI updates. The OCR layer is isolated so it can be replaced by Tesseract, EasyOCR, PaddleOCR, docTR or an external OCR/LLM API without changing the document endpoints.

## JWT Auth

JWT Bearer auth keeps the API stateless and easy to consume from Next.js. Passwords are hashed, tokens expire, and document access is scoped by the authenticated user.

## Table Auto-Create Instead Of Alembic

For the local demo, the backend creates tables at startup to make `docker compose up --build` work from a clean checkout. In production, Alembic should be used to version database migrations and review schema changes explicitly.

## Ownership As Core Behavior

Document reads, status checks, OCR reads and deletes are filtered by `user_id`. If a document does not belong to the authenticated user, the API returns `404` so it does not reveal whether the document exists.

## File Validation

The API accepts only JPG, PNG and PDF files up to 10 MB. Validation happens before storing the file or creating metadata, reducing invalid records and avoiding unnecessary storage writes.
