from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models import Document, DocumentStatus, User
from app.services.storage_service import delete_file, upload_file


ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".pdf"}
ALLOWED_CONTENT_TYPES = {
    "image/jpeg",
    "image/png",
    "application/pdf",
}


def validate_upload(filename: str, content_type: str | None, file_size: int) -> None:
    settings = get_settings()
    extension = Path(filename).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only JPG, PNG and PDF files are allowed",
        )
    if content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file content type",
        )
    if file_size == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty",
        )
    if file_size > settings.max_upload_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Uploaded file exceeds the maximum size",
        )


async def create_document(db: Session, current_user: User, file: UploadFile) -> Document:
    settings = get_settings()
    file_bytes = await file.read()
    filename = file.filename or "document"
    validate_upload(filename, file.content_type, len(file_bytes))

    extension = Path(filename).suffix.lower()
    object_name = f"{current_user.id}/{uuid4().hex}{extension}"
    upload_file(object_name, file_bytes, file.content_type or "application/octet-stream")

    document = Document(
        user_id=current_user.id,
        original_filename=filename,
        content_type=file.content_type or "application/octet-stream",
        size_bytes=len(file_bytes),
        bucket_name=settings.minio_bucket,
        object_name=object_name,
        status=DocumentStatus.UPLOADED,
    )
    db.add(document)
    db.commit()
    db.refresh(document)

    from app.workers.tasks import process_document_ocr

    process_document_ocr.delay(document.id)
    return document


def delete_document(db: Session, document: Document) -> None:
    delete_file(document.bucket_name, document.object_name)
    db.delete(document)
    db.commit()
