from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models import Document, User
from app.repositories.document_repository import (
    get_document_for_user,
    list_documents_for_user,
)
from app.schemas.document import (
    DocumentCreateResponse,
    DocumentOcrResponse,
    DocumentRead,
    DocumentStatusResponse,
)
from app.services.document_service import create_document, delete_document


router = APIRouter(prefix="/documents", tags=["documents"])


def require_document(db: Session, document_id: int, user_id: int) -> Document:
    document = get_document_for_user(db, document_id, user_id)
    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )
    return document


@router.post("", response_model=DocumentCreateResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Document:
    return await create_document(db, current_user, file)


@router.get("", response_model=list[DocumentRead])
def list_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Document]:
    return list_documents_for_user(db, current_user.id)


@router.get("/{document_id}", response_model=DocumentRead)
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Document:
    return require_document(db, document_id, current_user.id)


@router.get("/{document_id}/status", response_model=DocumentStatusResponse)
def get_document_status(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> DocumentStatusResponse:
    document = require_document(db, document_id, current_user.id)
    return DocumentStatusResponse(
        id=document.id,
        status=document.status,
        error_message=document.error_message,
    )


@router.get("/{document_id}/ocr", response_model=DocumentOcrResponse)
def get_document_ocr(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> DocumentOcrResponse:
    document = require_document(db, document_id, current_user.id)
    return DocumentOcrResponse(
        id=document.id,
        status=document.status,
        ocr_text=document.ocr_text,
        error_message=document.error_message,
    )


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    document = require_document(db, document_id, current_user.id)
    delete_document(db, document)
