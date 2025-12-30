"""User routes"""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserRead, UserUpdate
from app.crud.user import get_user_by_id, update_user
from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: UUID, db: Session = Depends(get_db)):
    """Get user profile by ID"""
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@router.get("/me", response_model=UserRead)
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Get current authenticated user profile"""
    return current_user


@router.put("/{user_id}", response_model=UserRead)
async def update_user_profile(
    user_id: UUID,
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update user profile (only own profile)"""
    # Users can only update their own profile
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot update other users' profiles",
        )
    
    user = await update_user(db, user_id, user_in)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user

