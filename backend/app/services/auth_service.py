from sqlalchemy.orm import Session

from app.core.security import create_access_token, verify_password
from app.models import User
from app.repositories.user_repository import get_user_by_email


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.password_hash):
        return None
    return user


def build_access_token(user: User) -> str:
    return create_access_token(subject=str(user.id))
