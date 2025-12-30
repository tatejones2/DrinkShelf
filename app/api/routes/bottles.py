"""Bottle API routes"""

from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.bottle import BottleCreate, BottleRead, BottleUpdate
from app.crud.bottle import (
    create_bottle,
    get_bottle_by_id,
    get_user_bottles,
    get_user_bottles_count,
    update_bottle,
    soft_delete_bottle,
    update_bottle_ai_details,
)
from app.dependencies import get_current_user
from app.models.user import User
from app.services.ai_service import research_bottle

router = APIRouter(prefix="/bottles", tags=["bottles"])


@router.post("", response_model=BottleRead, status_code=status.HTTP_201_CREATED)
async def create_new_bottle(
    bottle_in: BottleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new bottle entry"""
    bottle = await create_bottle(db, current_user.id, bottle_in)
    
    # Optionally trigger AI research
    if bottle_in.research:
        ai_details = await research_bottle(bottle_in.name, bottle_in.distillery, bottle_in.spirit_type.value)
        if ai_details:
            bottle = await update_bottle_ai_details(db, bottle.id, current_user.id, ai_details)
    
    return bottle


@router.get("", response_model=list[BottleRead])
async def list_user_bottles(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    spirit_type: Optional[str] = None,
    min_rating: Optional[int] = Query(None, ge=1, le=5),
):
    """List user's bottles with optional filtering"""
    bottles = await get_user_bottles(
        db,
        current_user.id,
        skip=skip,
        limit=limit,
        spirit_type=spirit_type,
        min_rating=min_rating,
    )
    return bottles


@router.get("/stats")
async def get_bottle_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get statistics about user's bottle collection"""
    from sqlalchemy import func
    from app.models.bottle import Bottle
    
    total_bottles = await get_user_bottles_count(db, current_user.id)
    
    # Get spirit type breakdown
    spirit_breakdown = db.query(
        Bottle.spirit_type,
        func.count(Bottle.id).label("count")
    ).filter(
        Bottle.user_id == current_user.id,
        Bottle.deleted_at == None
    ).group_by(Bottle.spirit_type).all()
    
    # Get average rating
    avg_rating = db.query(
        func.avg(Bottle.rating)
    ).filter(
        Bottle.user_id == current_user.id,
        Bottle.deleted_at == None,
        Bottle.rating != None
    ).scalar()
    
    return {
        "total_bottles": total_bottles,
        "average_rating": float(avg_rating) if avg_rating else None,
        "spirit_breakdown": [
            {"spirit_type": str(spirit), "count": count}
            for spirit, count in spirit_breakdown
        ],
    }


@router.get("/{bottle_id}", response_model=BottleRead)
async def get_bottle(
    bottle_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get specific bottle details (must be owner)"""
    bottle = await get_bottle_by_id(db, bottle_id, current_user.id)
    if not bottle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bottle not found",
        )
    return bottle


@router.put("/{bottle_id}", response_model=BottleRead)
async def update_bottle_info(
    bottle_id: UUID,
    bottle_in: BottleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update bottle information (must be owner)"""
    bottle = await update_bottle(db, bottle_id, current_user.id, bottle_in)
    if not bottle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bottle not found",
        )
    return bottle


@router.delete("/{bottle_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bottle(
    bottle_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a bottle (soft delete, must be owner)"""
    success = await soft_delete_bottle(db, bottle_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bottle not found",
        )
