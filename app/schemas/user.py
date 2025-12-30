"""User schemas"""

from typing import Optional
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Base user schema"""

    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    display_name: Optional[str] = Field(None, max_length=100)
    bio: Optional[str] = None


class UserCreate(UserBase):
    """Schema for user registration"""

    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    """Schema for updating user profile"""

    display_name: Optional[str] = Field(None, max_length=100)
    bio: Optional[str] = None


class UserRead(UserBase):
    """Schema for reading user data"""

    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
