"""Tasting Note API routes"""

from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.tasting_note import TastingNoteCreate, TastingNoteRead, TastingNoteUpdate
from app.crud.tasting_note import (
    create_tasting_note,
    get_tasting_note_by_id,
    get_bottle_tasting_notes,
    get_user_tasting_notes,
    update_tasting_note,
    delete_tasting_note,
    get_bottle_average_rating,
    get_bottle_tasting_note_count,
    get_user_tasting_statistics,
)
from app.crud.bottle import get_bottle_by_id as get_bottle
from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/tasting-notes", tags=["tasting-notes"])


@router.post("/bottles/{bottle_id}", response_model=TastingNoteRead, status_code=status.HTTP_201_CREATED)
async def create_bottle_tasting_note(
    bottle_id: UUID,
    tasting_note_in: TastingNoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a tasting note for a bottle"""
    # Verify bottle exists and user owns it
    bottle = await get_bottle(db, bottle_id, current_user.id)
    if not bottle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bottle not found",
        )
    
    tasting_note = await create_tasting_note(
        db, bottle_id, current_user.id, tasting_note_in
    )
    return tasting_note


@router.get("/bottles/{bottle_id}", response_model=list[TastingNoteRead])
async def list_bottle_tasting_notes(
    bottle_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
):
    """List tasting notes for a bottle (only user's own notes)"""
    # Verify bottle exists and user owns it
    bottle = await get_bottle(db, bottle_id, current_user.id)
    if not bottle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bottle not found",
        )
    
    notes = await get_bottle_tasting_notes(
        db, bottle_id, skip=skip, limit=limit, user_id=current_user.id
    )
    return notes


@router.get("/{tasting_note_id}", response_model=TastingNoteRead)
async def get_tasting_note(
    tasting_note_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get specific tasting note (must be owner)"""
    note = await get_tasting_note_by_id(db, tasting_note_id, current_user.id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tasting note not found",
        )
    return note


@router.put("/{tasting_note_id}", response_model=TastingNoteRead)
async def update_tasting_note_endpoint(
    tasting_note_id: UUID,
    tasting_note_in: TastingNoteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update tasting note (must be owner)"""
    note = await update_tasting_note(db, tasting_note_id, current_user.id, tasting_note_in)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tasting note not found",
        )
    return note


@router.delete("/{tasting_note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tasting_note_endpoint(
    tasting_note_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete tasting note (must be owner)"""
    success = await delete_tasting_note(db, tasting_note_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tasting note not found",
        )


@router.get("/user/statistics")
async def get_user_tasting_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get user's tasting statistics"""
    stats = await get_user_tasting_statistics(db, current_user.id)
    return stats


@router.get("/bottle/{bottle_id}/stats")
async def get_bottle_tasting_stats(
    bottle_id: UUID,
    db: Session = Depends(get_db),
):
    """Get tasting statistics for a bottle (public)"""
    avg_rating = await get_bottle_average_rating(db, bottle_id)
    note_count = await get_bottle_tasting_note_count(db, bottle_id)
    
    return {
        "bottle_id": bottle_id,
        "average_rating": avg_rating,
        "total_tasting_notes": note_count,
    }


@router.get("/user/{user_id}/notes", response_model=list[TastingNoteRead])
async def get_user_notes(
    user_id: UUID,
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
):
    """Get user's tasting notes (public profile)"""
    notes = await get_user_tasting_notes(db, user_id, skip=skip, limit=limit)
    if not notes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found or has no tasting notes",
        )
    return notes
