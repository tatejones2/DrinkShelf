"""Bottle model"""

from datetime import datetime, date
from uuid import uuid4
from enum import Enum
from sqlalchemy import (
    Column,
    String,
    Text,
    Float,
    Integer,
    Date,
    DateTime,
    ForeignKey,
    Numeric,
    JSON,
)
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.orm import relationship
from app.database.base import Base


class SpiritType(str, Enum):
    """Spirit type enumeration"""

    WHISKEY = "whiskey"
    VODKA = "vodka"
    TEQUILA = "tequila"
    RUM = "rum"
    GIN = "gin"
    BEER = "beer"
    WINE = "wine"
    LIQUEUR = "liqueur"
    OTHER = "other"


class Bottle(Base):
    """Bottle model for spirit collection"""

    __tablename__ = "bottles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True
    )
    name = Column(String(255), nullable=False, index=True)
    spirit_type = Column(ENUM(SpiritType), nullable=False, index=True)
    distillery = Column(String(255), nullable=True, index=True)
    proof = Column(Float, nullable=True)
    age_statement = Column(String(50), nullable=True)
    region = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True, index=True)
    release_year = Column(Integer, nullable=True)
    batch_number = Column(String(100), nullable=True)
    price_paid = Column(Numeric(10, 2), nullable=True)
    price_current = Column(Numeric(10, 2), nullable=True)
    acquisition_date = Column(Date, nullable=True)
    notes = Column(Text, nullable=True)
    rating = Column(Integer, nullable=True)  # 1-5 scale
    image_url = Column(String(500), nullable=True)
    ai_details = Column(JSON, nullable=True)  # Stores OpenAI-generated details
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    deleted_at = Column(DateTime, nullable=True, index=True)  # Soft delete

    # Relationships
    user = relationship("User", back_populates="bottles")
    tasting_notes = relationship(
        "TastingNote", back_populates="bottle", cascade="all, delete-orphan"
    )
    collections = relationship(
        "Collection",
        secondary="collection_bottles",
        back_populates="bottles",
    )

    def __repr__(self) -> str:
        return f"<Bottle(id={self.id}, name={self.name}, spirit_type={self.spirit_type})>"
