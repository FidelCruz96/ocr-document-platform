from sqlalchemy.orm import Session

from app.repositories.document_repository import (
    get_document_for_user,
    list_documents_for_user,
)

from conftest import create_document, create_user


def test_get_document_for_user_returns_owned_document(db: Session) -> None:
    user = create_user(db)
    document = create_document(db, user)

    found_document = get_document_for_user(db, document.id, user.id)

    assert found_document is not None
    assert found_document.id == document.id


def test_get_document_for_user_hides_other_user_document(db: Session) -> None:
    owner = create_user(db, "owner@test.com")
    other_user = create_user(db, "other@test.com")
    document = create_document(db, owner)

    found_document = get_document_for_user(db, document.id, other_user.id)

    assert found_document is None


def test_list_documents_for_user_only_returns_owned_documents(db: Session) -> None:
    owner = create_user(db, "owner@test.com")
    other_user = create_user(db, "other@test.com")
    owned_document = create_document(db, owner, "owned.pdf")
    create_document(db, other_user, "other.pdf")

    documents = list_documents_for_user(db, owner.id)

    assert [document.id for document in documents] == [owned_document.id]
