from sqlalchemy.orm import Session

from app.services.auth_service import authenticate_user

from conftest import create_user


def test_authenticate_user_accepts_valid_credentials(db: Session) -> None:
    user = create_user(db)

    authenticated_user = authenticate_user(db, user.email, "password123")

    assert authenticated_user is not None
    assert authenticated_user.id == user.id


def test_authenticate_user_rejects_invalid_credentials(db: Session) -> None:
    user = create_user(db)

    authenticated_user = authenticate_user(db, user.email, "wrong-password")

    assert authenticated_user is None
