"""Collection models"""

from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer, Table, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database.base import Base


# Association table for many-to-many relationship between collections and bottles
collection_bottles = Table(
    "collection_bottles",
    Base.metadata,
    Column("collection_id", UUID(as_uuid=True), ForeignKey("collections.id"), primary_key=True),
    Column("bottle_id", UUID(as_uuid=True), ForeignKey("bottles.id"), primary_key=True),
    Column("position", Integer, nullable=True),
    Column("added_at", DateTime, default=datetime.utcnow),
)


class Collection(Base):
    """Collection model for organizing bottles"""

    __tablename__ = "collections"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True
    )
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    user = relationship("User", back_populates="collections")
    bottles = relationship(
        "Bottle",
        secondary=collection_bottles,
        back_populates="collections",
    )

    def __repr__(self) -> str:
        return f"<Collection(id={self.id}, name={self.name})>"


class CollectionBottle(Base):
    """Collection-Bottle association model (if needed for extra fields)"""

    __tablename__ = "collection_bottles"
    __table_args__ = ()  # Uses the association table defined above

    # Note: This model is optional. The association table handles the relationship.
    # This exists if we need to add additional metadata to the relationship.
