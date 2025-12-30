"""Tasting note model"""

from datetime import datetime, date
from uuid import uuid4
from sqlalchemy import Column, Text, Integer, Date, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database.base import Base


class TastingNote(Base):
    """Tasting note model for bottles"""

    __tablename__ = "tasting_notes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    bottle_id = Column(
        UUID(as_uuid=True), ForeignKey("bottles.id"), nullable=False, index=True
    )
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True
    )
    nose = Column(Text, nullable=True)
    palate = Column(Text, nullable=True)
    finish = Column(Text, nullable=True)
    overall_notes = Column(Text, nullable=True)
    rating = Column(Integer, nullable=True)  # 1-5 scale
    tasted_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    bottle = relationship("Bottle", back_populates="tasting_notes")
    user = relationship("User", back_populates="tasting_notes")

    def __repr__(self) -> str:
        return f"<TastingNote(id={self.id}, bottle_id={self.bottle_id}, rating={self.rating})>"
