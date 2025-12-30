"""Bottle CRUD operations"""

from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.bottle import Bottle
from app.schemas.bottle import BottleCreate, BottleUpdate


async def create_bottle(db: Session, user_id: UUID, bottle_in: BottleCreate) -> Bottle:
    """Create a new bottle entry"""
    db_bottle = Bottle(
        user_id=user_id,
        name=bottle_in.name,
        spirit_type=bottle_in.spirit_type,
        distillery=bottle_in.distillery,
        proof=bottle_in.proof,
        age_statement=bottle_in.age_statement,
        region=bottle_in.region,
        country=bottle_in.country,
        release_year=bottle_in.release_year,
        batch_number=bottle_in.batch_number,
        price_paid=bottle_in.price_paid,
        price_current=bottle_in.price_current,
        acquisition_date=bottle_in.acquisition_date,
        notes=bottle_in.notes,
        rating=bottle_in.rating,
        image_url=bottle_in.image_url,
    )
    db.add(db_bottle)
    db.commit()
    db.refresh(db_bottle)
    return db_bottle


async def get_bottle_by_id(db: Session, bottle_id: UUID, user_id: Optional[UUID] = None) -> Optional[Bottle]:
    """Get bottle by ID, optionally filtered by user"""
    query = db.query(Bottle).filter(
        Bottle.id == bottle_id,
        Bottle.deleted_at == None
    )
    if user_id:
        query = query.filter(Bottle.user_id == user_id)
    return query.first()


async def get_user_bottles(
    db: Session,
    user_id: UUID,
    skip: int = 0,
    limit: int = 50,
    spirit_type: Optional[str] = None,
    min_rating: Optional[int] = None,
) -> List[Bottle]:
    """Get all bottles for a user with optional filtering"""
    query = db.query(Bottle).filter(
        Bottle.user_id == user_id,
        Bottle.deleted_at == None
    )
    
    if spirit_type:
        query = query.filter(Bottle.spirit_type == spirit_type)
    
    if min_rating is not None:
        query = query.filter(Bottle.rating >= min_rating)
    
    return query.order_by(Bottle.created_at.desc()).offset(skip).limit(limit).all()


async def get_user_bottles_count(
    db: Session,
    user_id: UUID,
    spirit_type: Optional[str] = None,
) -> int:
    """Get count of user's bottles with optional filtering"""
    query = db.query(Bottle).filter(
        Bottle.user_id == user_id,
        Bottle.deleted_at == None
    )
    
    if spirit_type:
        query = query.filter(Bottle.spirit_type == spirit_type)
    
    return query.count()


async def update_bottle(db: Session, bottle_id: UUID, user_id: UUID, bottle_in: BottleUpdate) -> Optional[Bottle]:
    """Update bottle (must be owner)"""
    db_bottle = await get_bottle_by_id(db, bottle_id, user_id)
    if not db_bottle:
        return None
    
    update_data = bottle_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_bottle, field, value)
    
    db.add(db_bottle)
    db.commit()
    db.refresh(db_bottle)
    return db_bottle


async def soft_delete_bottle(db: Session, bottle_id: UUID, user_id: UUID) -> bool:
    """Soft delete a bottle (mark as deleted, don't remove)"""
    from datetime import datetime
    
    db_bottle = await get_bottle_by_id(db, bottle_id, user_id)
    if not db_bottle:
        return False
    
    db_bottle.deleted_at = datetime.utcnow()
    db.add(db_bottle)
    db.commit()
    return True


async def update_bottle_ai_details(
    db: Session,
    bottle_id: UUID,
    user_id: UUID,
    ai_details: dict
) -> Optional[Bottle]:
    """Update bottle with AI research details"""
    db_bottle = await get_bottle_by_id(db, bottle_id, user_id)
    if not db_bottle:
        return None
    
    db_bottle.ai_details = ai_details
    db.add(db_bottle)
    db.commit()
    db.refresh(db_bottle)
    return db_bottle
