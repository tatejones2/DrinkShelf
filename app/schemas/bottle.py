"""Bottle schemas"""

from typing import Optional
from datetime import datetime, date
from uuid import UUID
from decimal import Decimal
from pydantic import BaseModel, Field
from app.models.bottle import SpiritType


class BottleBase(BaseModel):
    """Base bottle schema"""

    name: str = Field(..., min_length=1, max_length=255)
    spirit_type: SpiritType
    distillery: Optional[str] = Field(None, max_length=255)
    proof: Optional[float] = Field(None, ge=0, le=200)
    age_statement: Optional[str] = Field(None, max_length=50)
    region: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=100)
    release_year: Optional[int] = Field(None, ge=1800, le=2100)
    batch_number: Optional[str] = Field(None, max_length=100)
    price_paid: Optional[Decimal] = Field(None, decimal_places=2)
    price_current: Optional[Decimal] = Field(None, decimal_places=2)
    acquisition_date: Optional[date] = None
    notes: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=5)
    image_url: Optional[str] = Field(None, max_length=500)


class BottleCreate(BottleBase):
    """Schema for creating a bottle"""

    research: Optional[bool] = False  # Flag to trigger AI research


class BottleUpdate(BaseModel):
    """Schema for updating a bottle"""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    spirit_type: Optional[SpiritType] = None
    distillery: Optional[str] = Field(None, max_length=255)
    proof: Optional[float] = Field(None, ge=0, le=200)
    age_statement: Optional[str] = Field(None, max_length=50)
    region: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=100)
    release_year: Optional[int] = Field(None, ge=1800, le=2100)
    batch_number: Optional[str] = Field(None, max_length=100)
    price_paid: Optional[Decimal] = Field(None, decimal_places=2)
    price_current: Optional[Decimal] = Field(None, decimal_places=2)
    acquisition_date: Optional[date] = None
    notes: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=5)
    image_url: Optional[str] = Field(None, max_length=500)


class BottleRead(BottleBase):
    """Schema for reading bottle data"""

    id: UUID
    user_id: UUID
    ai_details: Optional[dict] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
