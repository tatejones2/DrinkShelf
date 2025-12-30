"""Tasting Note CRUD operations"""

from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.tasting_note import TastingNote
from app.schemas.tasting_note import TastingNoteCreate, TastingNoteUpdate


async def create_tasting_note(
    db: Session,
    bottle_id: UUID,
    user_id: UUID,
    tasting_note_in: TastingNoteCreate,
) -> TastingNote:
    """Create a new tasting note for a bottle"""
    db_note = TastingNote(
        bottle_id=bottle_id,
        user_id=user_id,
        nose=tasting_note_in.nose,
        palate=tasting_note_in.palate,
        finish=tasting_note_in.finish,
        overall_notes=tasting_note_in.overall_notes,
        rating=tasting_note_in.rating,
        tasted_date=tasting_note_in.tasted_date,
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


async def get_tasting_note_by_id(
    db: Session,
    tasting_note_id: UUID,
    user_id: Optional[UUID] = None,
) -> Optional[TastingNote]:
    """Get tasting note by ID, optionally filtered by user"""
    query = db.query(TastingNote).filter(TastingNote.id == tasting_note_id)
    if user_id:
        query = query.filter(TastingNote.user_id == user_id)
    return query.first()


async def get_bottle_tasting_notes(
    db: Session,
    bottle_id: UUID,
    skip: int = 0,
    limit: int = 50,
    user_id: Optional[UUID] = None,  # If provided, get only user's notes
) -> List[TastingNote]:
    """Get tasting notes for a bottle"""
    query = db.query(TastingNote).filter(TastingNote.bottle_id == bottle_id)
    
    if user_id:
        query = query.filter(TastingNote.user_id == user_id)
    
    return query.order_by(TastingNote.created_at.desc()).offset(skip).limit(limit).all()


async def get_user_tasting_notes(
    db: Session,
    user_id: UUID,
    skip: int = 0,
    limit: int = 50,
) -> List[TastingNote]:
    """Get all tasting notes created by a user"""
    return db.query(TastingNote).filter(
        TastingNote.user_id == user_id
    ).order_by(TastingNote.created_at.desc()).offset(skip).limit(limit).all()


async def update_tasting_note(
    db: Session,
    tasting_note_id: UUID,
    user_id: UUID,
    tasting_note_in: TastingNoteUpdate,
) -> Optional[TastingNote]:
    """Update tasting note (must be owner)"""
    db_note = await get_tasting_note_by_id(db, tasting_note_id, user_id)
    if not db_note:
        return None
    
    update_data = tasting_note_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_note, field, value)
    
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


async def delete_tasting_note(
    db: Session,
    tasting_note_id: UUID,
    user_id: UUID,
) -> bool:
    """Delete tasting note (must be owner)"""
    db_note = await get_tasting_note_by_id(db, tasting_note_id, user_id)
    if not db_note:
        return False
    
    db.delete(db_note)
    db.commit()
    return True


async def get_bottle_average_rating(
    db: Session,
    bottle_id: UUID,
) -> Optional[float]:
    """Get average rating for a bottle from all tasting notes"""
    from sqlalchemy import func
    
    avg_rating = db.query(
        func.avg(TastingNote.rating)
    ).filter(
        TastingNote.bottle_id == bottle_id,
        TastingNote.rating != None,
    ).scalar()
    
    return float(avg_rating) if avg_rating else None


async def get_bottle_tasting_note_count(
    db: Session,
    bottle_id: UUID,
) -> int:
    """Get count of tasting notes for a bottle"""
    return db.query(TastingNote).filter(
        TastingNote.bottle_id == bottle_id
    ).count()


async def get_user_tasting_statistics(
    db: Session,
    user_id: UUID,
) -> dict:
    """Get tasting statistics for a user"""
    from sqlalchemy import func
    
    # Total tasting notes
    total_notes = db.query(TastingNote).filter(
        TastingNote.user_id == user_id
    ).count()
    
    # Average rating given
    avg_rating = db.query(
        func.avg(TastingNote.rating)
    ).filter(
        TastingNote.user_id == user_id,
        TastingNote.rating != None,
    ).scalar()
    
    # Most tasted spirit type (join with bottles)
    from app.models.bottle import Bottle
    most_tasted = db.query(
        Bottle.spirit_type,
        func.count(TastingNote.id).label("count")
    ).join(
        Bottle, TastingNote.bottle_id == Bottle.id
    ).filter(
        TastingNote.user_id == user_id
    ).group_by(Bottle.spirit_type).order_by(func.count(TastingNote.id).desc()).first()
    
    return {
        "total_tasting_notes": total_notes,
        "average_rating": float(avg_rating) if avg_rating else None,
        "most_tasted_spirit": str(most_tasted[0]) if most_tasted else None,
        "most_tasted_count": most_tasted[1] if most_tasted else 0,
    }
