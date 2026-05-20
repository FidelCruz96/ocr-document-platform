from collections.abc import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.security import get_password_hash
from app.db.base import Base
from app.models import Document, DocumentStatus, User


@pytest.fixture
def db() -> Generator[Session, None, None]:
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


def create_user(db: Session, email: str = "user@test.com") -> User:
    user = User(email=email, password_hash=get_password_hash("password123"))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_document(
    db: Session,
    user: User,
    filename: str = "sample.pdf",
    status: str = DocumentStatus.UPLOADED,
) -> Document:
    document = Document(
        user_id=user.id,
        original_filename=filename,
        content_type="application/pdf",
        size_bytes=100,
        bucket_name="documents",
        object_name=f"{user.id}/{filename}",
        status=status,
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    return document
