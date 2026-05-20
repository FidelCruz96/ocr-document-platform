from sqlalchemy.orm import Session

from app.models import DocumentStatus
from app.workers import tasks

from conftest import create_document, create_user


class SuccessfulOCRProvider:
    def extract_text(self, file_bytes: bytes, content_type: str) -> str:
        return "worker OCR text"


def test_process_document_marks_document_completed(
    db: Session, monkeypatch
) -> None:
    user = create_user(db)
    document = create_document(db, user)
    monkeypatch.setattr(tasks, "download_file", lambda bucket, object_name: b"bytes")
    monkeypatch.setattr(tasks, "get_ocr_provider", lambda: SuccessfulOCRProvider())

    tasks.process_document(db, document.id)

    db.refresh(document)
    assert document.status == DocumentStatus.COMPLETED
    assert document.ocr_text == "worker OCR text"
    assert document.error_message is None
    assert document.processed_at is not None


def test_process_document_skips_completed_document(
    db: Session, monkeypatch
) -> None:
    user = create_user(db)
    document = create_document(db, user, status=DocumentStatus.COMPLETED)
    document.ocr_text = "existing text"
    db.commit()
    monkeypatch.setattr(
        tasks,
        "download_file",
        lambda bucket, object_name: (_ for _ in ()).throw(AssertionError("called")),
    )

    tasks.process_document(db, document.id)

    db.refresh(document)
    assert document.status == DocumentStatus.COMPLETED
    assert document.ocr_text == "existing text"


def test_mark_document_failed_records_error(db: Session) -> None:
    user = create_user(db)
    document = create_document(db, user)

    tasks.mark_document_failed(db, document.id, "temporary failure")

    db.refresh(document)
    assert document.status == DocumentStatus.FAILED
    assert document.error_message == "temporary failure"
    assert document.processed_at is not None


def test_mark_document_failed_does_not_overwrite_completed_document(db: Session) -> None:
    user = create_user(db)
    document = create_document(db, user, status=DocumentStatus.COMPLETED)
    document.ocr_text = "final text"
    db.commit()

    tasks.mark_document_failed(db, document.id, "late failure")

    db.refresh(document)
    assert document.status == DocumentStatus.COMPLETED
    assert document.ocr_text == "final text"
    assert document.error_message is None
