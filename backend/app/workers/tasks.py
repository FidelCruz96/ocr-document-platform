from datetime import datetime, timezone
from typing import Any

from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models import Document, DocumentStatus
from app.services.ocr_service import get_ocr_provider
from app.services.storage_service import download_file
from app.workers.celery_app import celery_app


def mark_document_failed(db: Session, document_id: int, error_message: str) -> None:
    document = db.query(Document).filter(Document.id == document_id).first()
    if document is None:
        return
    if document.status == DocumentStatus.COMPLETED:
        return
    document.status = DocumentStatus.FAILED
    document.error_message = error_message
    document.processed_at = datetime.now(timezone.utc)
    db.commit()


def process_document(db: Session, document_id: int) -> None:
    document = db.query(Document).filter(Document.id == document_id).first()
    if document is None:
        return
    if document.status == DocumentStatus.COMPLETED:
        return

    document.status = DocumentStatus.PROCESSING
    document.error_message = None
    db.commit()
    db.refresh(document)

    file_bytes = download_file(document.bucket_name, document.object_name)
    document.ocr_text = get_ocr_provider().extract_text(file_bytes, document.content_type)
    document.status = DocumentStatus.COMPLETED
    document.processed_at = datetime.now(timezone.utc)
    db.commit()


@celery_app.task(
    bind=True,
    name="process_document_ocr",
    max_retries=3,
    default_retry_delay=10,
)
def process_document_ocr(self: Any, document_id: int) -> None:
    db = SessionLocal()
    try:
        process_document(db, document_id)
    except Exception as exc:
        db.rollback()
        if self.request.retries < self.max_retries:
            raise self.retry(exc=exc)
        mark_document_failed(db, document_id, str(exc))
    finally:
        db.close()
