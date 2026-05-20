from datetime import datetime
from typing import Literal

from pydantic import BaseModel


DocumentStatusValue = Literal["uploaded", "processing", "completed", "failed"]


class DocumentRead(BaseModel):
    id: int
    original_filename: str
    content_type: str
    size_bytes: int
    status: DocumentStatusValue
    error_message: str | None
    created_at: datetime
    updated_at: datetime
    processed_at: datetime | None

    model_config = {"from_attributes": True}


class DocumentCreateResponse(BaseModel):
    id: int
    status: DocumentStatusValue


class DocumentStatusResponse(BaseModel):
    id: int
    status: DocumentStatusValue
    error_message: str | None = None


class DocumentOcrResponse(BaseModel):
    id: int
    status: DocumentStatusValue
    ocr_text: str | None = None
    error_message: str | None = None
