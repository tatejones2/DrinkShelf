"""Tasting note schemas"""

from typing import Optional
from datetime import datetime, date
from uuid import UUID
from pydantic import BaseModel, Field


class TastingNoteBase(BaseModel):
    """Base tasting note schema"""

    nose: Optional[str] = None
    palate: Optional[str] = None
    finish: Optional[str] = None
    overall_notes: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=5)
    tasted_date: Optional[date] = None


class TastingNoteCreate(TastingNoteBase):
    """Schema for creating a tasting note"""

    pass


class TastingNoteUpdate(BaseModel):
    """Schema for updating a tasting note"""

    nose: Optional[str] = None
    palate: Optional[str] = None
    finish: Optional[str] = None
    overall_notes: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=5)
    tasted_date: Optional[date] = None


class TastingNoteRead(TastingNoteBase):
    """Schema for reading tasting note data"""

    id: UUID
    bottle_id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
