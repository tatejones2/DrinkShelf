"""Collection CRUD operations"""

from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.collection import Collection
from app.schemas.collection import CollectionCreate, CollectionUpdate


async def create_collection(db: Session, user_id: UUID, collection_in: CollectionCreate) -> Collection:
    """Create a new collection"""
    db_collection = Collection(
        user_id=user_id,
        name=collection_in.name,
        description=collection_in.description,
        is_public=collection_in.is_public,
    )
    db.add(db_collection)
    db.commit()
    db.refresh(db_collection)
    return db_collection


async def get_collection_by_id(db: Session, collection_id: UUID, user_id: Optional[UUID] = None) -> Optional[Collection]:
    """Get collection by ID, optionally filtered by owner"""
    query = db.query(Collection).filter(Collection.id == collection_id)
    if user_id:
        query = query.filter(Collection.user_id == user_id)
    return query.first()


async def get_user_collections(
    db: Session,
    user_id: UUID,
    skip: int = 0,
    limit: int = 50,
) -> List[Collection]:
    """Get all collections for a user"""
    return db.query(Collection).filter(
        Collection.user_id == user_id
    ).order_by(Collection.created_at.desc()).offset(skip).limit(limit).all()


async def get_public_collections(
    db: Session,
    skip: int = 0,
    limit: int = 50,
) -> List[Collection]:
    """Get all public collections"""
    return db.query(Collection).filter(
        Collection.is_public == True
    ).order_by(Collection.created_at.desc()).offset(skip).limit(limit).all()


async def update_collection(
    db: Session,
    collection_id: UUID,
    user_id: UUID,
    collection_in: CollectionUpdate
) -> Optional[Collection]:
    """Update collection (must be owner)"""
    db_collection = await get_collection_by_id(db, collection_id, user_id)
    if not db_collection:
        return None
    
    update_data = collection_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_collection, field, value)
    
    db.add(db_collection)
    db.commit()
    db.refresh(db_collection)
    return db_collection


async def delete_collection(db: Session, collection_id: UUID, user_id: UUID) -> bool:
    """Delete a collection (must be owner)"""
    db_collection = await get_collection_by_id(db, collection_id, user_id)
    if not db_collection:
        return False
    
    db.delete(db_collection)
    db.commit()
    return True


async def add_bottle_to_collection(
    db: Session,
    collection_id: UUID,
    bottle_id: UUID,
    user_id: UUID,
) -> bool:
    """Add a bottle to a collection"""
    db_collection = await get_collection_by_id(db, collection_id, user_id)
    if not db_collection:
        return False
    
    # Check if bottle already in collection
    from app.models.bottle import Bottle
    bottle = db.query(Bottle).filter(
        Bottle.id == bottle_id,
        Bottle.user_id == user_id,
        Bottle.deleted_at == None
    ).first()
    
    if not bottle or bottle in db_collection.bottles:
        return False
    
    db_collection.bottles.append(bottle)
    db.add(db_collection)
    db.commit()
    return True


async def remove_bottle_from_collection(
    db: Session,
    collection_id: UUID,
    bottle_id: UUID,
    user_id: UUID,
) -> bool:
    """Remove a bottle from a collection"""
    db_collection = await get_collection_by_id(db, collection_id, user_id)
    if not db_collection:
        return False
    
    from app.models.bottle import Bottle
    bottle = db.query(Bottle).filter(Bottle.id == bottle_id).first()
    
    if not bottle or bottle not in db_collection.bottles:
        return False
    
    db_collection.bottles.remove(bottle)
    db.add(db_collection)
    db.commit()
    return True
