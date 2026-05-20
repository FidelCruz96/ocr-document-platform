import pytest
from fastapi import HTTPException

from app.services.document_service import validate_upload


def test_validate_upload_accepts_pdf() -> None:
    validate_upload("sample.pdf", "application/pdf", 10)


def test_validate_upload_rejects_invalid_extension() -> None:
    with pytest.raises(HTTPException):
        validate_upload("sample.exe", "application/octet-stream", 10)


def test_validate_upload_rejects_empty_file() -> None:
    with pytest.raises(HTTPException):
        validate_upload("sample.png", "image/png", 0)
