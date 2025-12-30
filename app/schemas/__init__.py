"""Pydantic schemas for request/response validation"""

from .user import UserCreate, UserRead, UserUpdate
from .bottle import BottleCreate, BottleRead, BottleUpdate
from .collection import CollectionCreate, CollectionRead, CollectionUpdate
from .tasting_note import TastingNoteCreate, TastingNoteRead, TastingNoteUpdate

__all__ = [
    "UserCreate",
    "UserRead",
    "UserUpdate",
    "BottleCreate",
    "BottleRead",
    "BottleUpdate",
    "CollectionCreate",
    "CollectionRead",
    "CollectionUpdate",
    "TastingNoteCreate",
    "TastingNoteRead",
    "TastingNoteUpdate",
]
