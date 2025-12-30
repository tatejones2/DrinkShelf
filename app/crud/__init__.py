"""User CRUD operations"""

from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.utils.security import get_password_hash, verify_password


async def create_user(db: Session, user_in: UserCreate) -> User:
    """Create a new user"""
    db_user = User(
        username=user_in.username,
        email=user_in.email,
        password_hash=get_password_hash(user_in.password),
        display_name=user_in.display_name,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


async def get_user_by_id(db: Session, user_id: UUID) -> Optional[User]:
    """Get user by ID"""
    return db.query(User).filter(User.id == user_id).first()


async def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Get user by username"""
    return db.query(User).filter(User.username == username).first()


async def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()


async def update_user(db: Session, user_id: UUID, user_in: UserUpdate) -> Optional[User]:
    """Update user profile"""
    db_user = await get_user_by_id(db, user_id)
    if not db_user:
        return None
    
    update_data = user_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


async def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """Authenticate user by username and password"""
    user = await get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user
