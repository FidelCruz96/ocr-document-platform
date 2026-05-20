from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import get_password_hash
from app.db.base import Base
from app.db.session import engine
from app.models import User


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


def seed_user(db: Session) -> None:
    settings = get_settings()
    existing_user = db.query(User).filter(User.email == settings.seed_user_email).first()
    if existing_user:
        return
    db.add(
        User(
            email=settings.seed_user_email,
            password_hash=get_password_hash(settings.seed_user_password),
        )
    )
    db.commit()
