from typing import Generator
from sqlalchemy.orm import Session

from app.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Dependencia que proporciona una sesión de base de datos.
    Se cierra automáticamente después de cada request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()