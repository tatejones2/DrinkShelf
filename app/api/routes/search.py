"""Search and discovery API routes"""

from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.bottle import BottleRead
from app.dependencies import get_current_user
from app.models.user import User
from app.services.search_service import (
    search_bottles,
    filter_bottles,
    get_popular_bottles,
    get_collection_stats,
    get_bottles_by_region,
    get_bottles_by_country,
    get_distillery_profile,
    get_price_range_stats,
)

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/bottles", response_model=list[BottleRead])
async def search_bottle_catalog(
    q: str = Query(..., min_length=1, max_length=100),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
):
    """Search bottles by name, distillery, region, or country"""
    bottles = await search_bottles(db, q, skip=skip, limit=limit)
    return bottles


@router.get("/filter", response_model=dict)
async def filter_bottle_catalog(
    db: Session = Depends(get_db),
    spirit_type: Optional[str] = None,
    min_proof: Optional[float] = Query(None, ge=0, le=200),
    max_proof: Optional[float] = Query(None, ge=0, le=200),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    region: Optional[str] = None,
    country: Optional[str] = None,
    min_rating: Optional[int] = Query(None, ge=1, le=5),
    max_rating: Optional[int] = Query(None, ge=1, le=5),
    year_from: Optional[int] = Query(None, ge=1800, le=2100),
    year_to: Optional[int] = Query(None, ge=1800, le=2100),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    sort_by: str = Query("created_at", regex="^(created_at|name|rating|price_paid)$"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
):
    """Advanced bottle filtering with multiple criteria"""
    from decimal import Decimal
    
    min_price_decimal = Decimal(min_price) if min_price else None
    max_price_decimal = Decimal(max_price) if max_price else None
    
    bottles, total_count = await filter_bottles(
        db,
        spirit_type=spirit_type,
        min_proof=min_proof,
        max_proof=max_proof,
        min_price=min_price_decimal,
        max_price=max_price_decimal,
        region=region,
        country=country,
        min_rating=min_rating,
        max_rating=max_rating,
        release_year_from=year_from,
        release_year_to=year_to,
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    
    return {
        "total": total_count,
        "count": len(bottles),
        "skip": skip,
        "limit": limit,
        "bottles": [
            {
                "id": b.id,
                "name": b.name,
                "spirit_type": b.spirit_type,
                "distillery": b.distillery,
                "proof": b.proof,
                "price_paid": float(b.price_paid) if b.price_paid else None,
                "region": b.region,
                "country": b.country,
                "rating": b.rating,
                "release_year": b.release_year,
            }
            for b in bottles
        ],
    }


@router.get("/popular", response_model=list[dict])
async def get_popular_spirits(
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1, le=50),
):
    """Get most popular bottles by community rating"""
    bottles = await get_popular_bottles(db, limit=limit)
    return bottles


@router.get("/stats")
async def get_catalog_statistics(
    db: Session = Depends(get_db),
):
    """Get overall collection statistics"""
    stats = await get_collection_stats(db)
    return stats


@router.get("/regions/{region}", response_model=list[BottleRead])
async def get_region_bottles(
    region: str,
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
):
    """Get all bottles from a specific region"""
    bottles = await get_bottles_by_region(db, region, skip=skip, limit=limit)
    return bottles


@router.get("/countries/{country}", response_model=list[BottleRead])
async def get_country_bottles(
    country: str,
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
):
    """Get all bottles from a specific country"""
    bottles = await get_bottles_by_country(db, country, skip=skip, limit=limit)
    return bottles


@router.get("/distillery/{distillery_name}")
async def get_distillery_info(
    distillery_name: str,
    db: Session = Depends(get_db),
):
    """Get profile information for a distillery"""
    profile = await get_distillery_profile(db, distillery_name)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Distillery not found",
        )
    return profile


@router.get("/pricing/stats")
async def get_pricing_statistics(
    db: Session = Depends(get_db),
):
    """Get price statistics across the collection"""
    stats = await get_price_range_stats(db)
    return stats
