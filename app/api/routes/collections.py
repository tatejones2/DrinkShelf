"""Collection API routes"""

from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.collection import CollectionCreate, CollectionRead, CollectionUpdate
from app.crud.collection import (
    create_collection,
    get_collection_by_id,
    get_user_collections,
    get_public_collections,
    update_collection,
    delete_collection,
    add_bottle_to_collection,
    remove_bottle_from_collection,
)
from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/collections", tags=["collections"])


@router.post("", response_model=CollectionRead, status_code=status.HTTP_201_CREATED)
async def create_new_collection(
    collection_in: CollectionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new collection"""
    collection = await create_collection(db, current_user.id, collection_in)
    return collection


@router.get("", response_model=list[CollectionRead])
async def list_user_collections(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
):
    """List user's collections"""
    collections = await get_user_collections(db, current_user.id, skip=skip, limit=limit)
    return collections


@router.get("/public", response_model=list[CollectionRead])
async def list_public_collections(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
):
    """List all public collections"""
    collections = await get_public_collections(db, skip=skip, limit=limit)
    return collections


@router.get("/{collection_id}", response_model=CollectionRead)
async def get_collection(
    collection_id: UUID,
    db: Session = Depends(get_db),
):
    """Get collection details (public collections don't require auth)"""
    collection = await get_collection_by_id(db, collection_id)
    if not collection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Collection not found",
        )
    return collection


@router.put("/{collection_id}", response_model=CollectionRead)
async def update_collection_info(
    collection_id: UUID,
    collection_in: CollectionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update collection (must be owner)"""
    collection = await update_collection(db, collection_id, current_user.id, collection_in)
    if not collection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Collection not found",
        )
    return collection


@router.delete("/{collection_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_collection_endpoint(
    collection_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a collection (must be owner)"""
    success = await delete_collection(db, collection_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Collection not found",
        )


@router.post("/{collection_id}/bottles/{bottle_id}", status_code=status.HTTP_204_NO_CONTENT)
async def add_bottle_to_collection_endpoint(
    collection_id: UUID,
    bottle_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Add a bottle to a collection"""
    success = await add_bottle_to_collection(db, collection_id, bottle_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Collection or bottle not found",
        )


@router.delete("/{collection_id}/bottles/{bottle_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_bottle_from_collection_endpoint(
    collection_id: UUID,
    bottle_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Remove a bottle from a collection"""
    success = await remove_bottle_from_collection(db, collection_id, bottle_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Collection or bottle not found",
        )
