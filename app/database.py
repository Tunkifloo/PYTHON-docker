from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

# Motor de base de datos
engine = create_engine(
    settings.database_url,
    echo=settings.DEBUG,  # Muestra SQL queries en consola
    pool_pre_ping=True,   # Verifica conexión antes de usar
    pool_size=10,         # Tamaño del pool de conexiones
    max_overflow=20       # Conexiones adicionales si es necesario
)

# Sesión de base de datos
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base para los modelos
Base = declarative_base()


def get_db():
    """
    Generador de sesiones de base de datos.
    Se usa como dependencia en los endpoints.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()