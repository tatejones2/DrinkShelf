"""Database session configuration"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Create database engine
if settings.DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=settings.ENVIRONMENT == "development",
    )
else:
    engine = create_engine(
        settings.DATABASE_URL,
        pool_size=settings.DATABASE_POOL_SIZE,
        max_overflow=settings.DATABASE_MAX_OVERFLOW,
        echo=settings.ENVIRONMENT == "development",
    )

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
