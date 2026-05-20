from datetime import datetime, timezone

from app.db.session import SessionLocal
from app.models import Document, DocumentStatus
from app.services.ocr_service import extract_text
from app.services.storage_service import download_file
from app.workers.celery_app import celery_app


@celery_app.task(name="process_document_ocr")
def process_document_ocr(document_id: int) -> None:
    db = SessionLocal()
    try:
        document = db.query(Document).filter(Document.id == document_id).first()
        if document is None:
            return

        document.status = DocumentStatus.PROCESSING
        document.error_message = None
        db.commit()
        db.refresh(document)

        file_bytes = download_file(document.bucket_name, document.object_name)
        document.ocr_text = extract_text(file_bytes, document.content_type)
        document.status = DocumentStatus.COMPLETED
        document.processed_at = datetime.now(timezone.utc)
        db.commit()
    except Exception as exc:
        db.rollback()
        document = db.query(Document).filter(Document.id == document_id).first()
        if document is not None:
            document.status = DocumentStatus.FAILED
            document.error_message = str(exc)
            document.processed_at = datetime.now(timezone.utc)
            db.commit()
        raise
    finally:
        db.close()
