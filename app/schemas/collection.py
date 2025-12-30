"""Collection schemas"""

from typing import Optional, List
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


class CollectionBase(BaseModel):
    """Base collection schema"""

    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    is_public: Optional[bool] = False


class CollectionCreate(CollectionBase):
    """Schema for creating a collection"""

    pass


class CollectionUpdate(BaseModel):
    """Schema for updating a collection"""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    is_public: Optional[bool] = None


class CollectionRead(CollectionBase):
    """Schema for reading collection data"""

    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
