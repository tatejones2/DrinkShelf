"""Search and discovery service for bottles"""

from typing import Optional, List, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from app.models.bottle import Bottle, SpiritType
from decimal import Decimal


async def search_bottles(
    db: Session,
    query: str,
    user_id: Optional[UUID] = None,
    skip: int = 0,
    limit: int = 50,
) -> List[Bottle]:
    """Search bottles by name, distillery, or region"""
    search_filter = or_(
        Bottle.name.ilike(f"%{query}%"),
        Bottle.distillery.ilike(f"%{query}%"),
        Bottle.region.ilike(f"%{query}%"),
        Bottle.country.ilike(f"%{query}%"),
    )
    
    base_query = db.query(Bottle).filter(
        search_filter,
        Bottle.deleted_at == None,
    )
    
    if user_id:
        base_query = base_query.filter(Bottle.user_id == user_id)
    
    return base_query.order_by(
        Bottle.created_at.desc()
    ).offset(skip).limit(limit).all()


async def filter_bottles(
    db: Session,
    user_id: Optional[UUID] = None,
    spirit_type: Optional[str] = None,
    min_proof: Optional[float] = None,
    max_proof: Optional[float] = None,
    min_price: Optional[Decimal] = None,
    max_price: Optional[Decimal] = None,
    region: Optional[str] = None,
    country: Optional[str] = None,
    min_rating: Optional[int] = None,
    max_rating: Optional[int] = None,
    release_year_from: Optional[int] = None,
    release_year_to: Optional[int] = None,
    skip: int = 0,
    limit: int = 50,
    sort_by: str = "created_at",
    sort_order: str = "desc",
) -> tuple[List[Bottle], int]:
    """Advanced filtering of bottles with multiple criteria"""
    query = db.query(Bottle).filter(Bottle.deleted_at == None)
    
    if user_id:
        query = query.filter(Bottle.user_id == user_id)
    
    if spirit_type:
        query = query.filter(Bottle.spirit_type == spirit_type)
    
    if min_proof is not None:
        query = query.filter(Bottle.proof >= min_proof)
    
    if max_proof is not None:
        query = query.filter(Bottle.proof <= max_proof)
    
    if min_price is not None:
        query = query.filter(Bottle.price_paid >= min_price)
    
    if max_price is not None:
        query = query.filter(Bottle.price_paid <= max_price)
    
    if region:
        query = query.filter(Bottle.region.ilike(f"%{region}%"))
    
    if country:
        query = query.filter(Bottle.country.ilike(f"%{country}%"))
    
    if min_rating is not None:
        query = query.filter(Bottle.rating >= min_rating)
    
    if max_rating is not None:
        query = query.filter(Bottle.rating <= max_rating)
    
    if release_year_from is not None:
        query = query.filter(Bottle.release_year >= release_year_from)
    
    if release_year_to is not None:
        query = query.filter(Bottle.release_year <= release_year_to)
    
    # Get total count before pagination
    total_count = query.count()
    
    # Sort
    sort_column = getattr(Bottle, sort_by, Bottle.created_at)
    if sort_order.lower() == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())
    
    # Pagination
    bottles = query.offset(skip).limit(limit).all()
    
    return bottles, total_count


async def get_popular_bottles(
    db: Session,
    limit: int = 10,
) -> List[Dict[str, Any]]:
    """Get most popular bottles (by rating)"""
    from app.models.tasting_note import TastingNote
    
    bottles = db.query(
        Bottle.id,
        Bottle.name,
        Bottle.spirit_type,
        Bottle.distillery,
        Bottle.rating,
        func.avg(TastingNote.rating).label("avg_community_rating"),
        func.count(TastingNote.id).label("total_reviews"),
    ).outerjoin(
        TastingNote, Bottle.id == TastingNote.bottle_id
    ).filter(
        Bottle.deleted_at == None,
        Bottle.rating != None,
    ).group_by(
        Bottle.id
    ).order_by(
        func.avg(TastingNote.rating).desc()
    ).limit(limit).all()
    
    return [
        {
            "id": b[0],
            "name": b[1],
            "spirit_type": str(b[2]),
            "distillery": b[3],
            "personal_rating": b[4],
            "community_rating": float(b[5]) if b[5] else None,
            "total_reviews": b[6],
        }
        for b in bottles
    ]


async def get_collection_stats(
    db: Session,
) -> Dict[str, Any]:
    """Get overall collection statistics"""
    total_bottles = db.query(func.count(Bottle.id)).filter(
        Bottle.deleted_at == None
    ).scalar()
    
    spirit_breakdown = db.query(
        Bottle.spirit_type,
        func.count(Bottle.id).label("count")
    ).filter(
        Bottle.deleted_at == None
    ).group_by(Bottle.spirit_type).all()
    
    avg_price = db.query(func.avg(Bottle.price_paid)).filter(
        Bottle.deleted_at == None,
        Bottle.price_paid != None,
    ).scalar()
    
    most_common = db.query(
        Bottle.spirit_type,
        func.count(Bottle.id).label("count")
    ).filter(
        Bottle.deleted_at == None
    ).group_by(Bottle.spirit_type).order_by(
        func.count(Bottle.id).desc()
    ).first()
    
    return {
        "total_bottles": total_bottles,
        "spirit_breakdown": [
            {"spirit_type": str(spirit), "count": count}
            for spirit, count in spirit_breakdown
        ],
        "average_price": float(avg_price) if avg_price else None,
        "most_common_spirit": str(most_common[0]) if most_common else None,
    }


async def get_bottles_by_region(
    db: Session,
    region: str,
    skip: int = 0,
    limit: int = 50,
) -> List[Bottle]:
    """Get all bottles from a specific region"""
    return db.query(Bottle).filter(
        Bottle.region.ilike(f"%{region}%"),
        Bottle.deleted_at == None,
    ).order_by(Bottle.rating.desc()).offset(skip).limit(limit).all()


async def get_bottles_by_country(
    db: Session,
    country: str,
    skip: int = 0,
    limit: int = 50,
) -> List[Bottle]:
    """Get all bottles from a specific country"""
    return db.query(Bottle).filter(
        Bottle.country.ilike(f"%{country}%"),
        Bottle.deleted_at == None,
    ).order_by(Bottle.rating.desc()).offset(skip).limit(limit).all()


async def get_distillery_profile(
    db: Session,
    distillery: str,
) -> Optional[Dict[str, Any]]:
    """Get profile data for a distillery"""
    bottles = db.query(Bottle).filter(
        Bottle.distillery.ilike(f"%{distillery}%"),
        Bottle.deleted_at == None,
    ).all()
    
    if not bottles:
        return None
    
    from app.models.tasting_note import TastingNote
    avg_rating = db.query(func.avg(TastingNote.rating)).join(
        Bottle, TastingNote.bottle_id == Bottle.id
    ).filter(
        Bottle.distillery.ilike(f"%{distillery}%")
    ).scalar()
    
    return {
        "distillery": distillery,
        "total_bottles": len(bottles),
        "countries": list(set(b.country for b in bottles if b.country)),
        "regions": list(set(b.region for b in bottles if b.region)),
        "average_rating": float(avg_rating) if avg_rating else None,
        "spirit_types": list(set(str(b.spirit_type) for b in bottles if b.spirit_type)),
    }


async def get_price_range_stats(
    db: Session,
) -> Dict[str, Any]:
    """Get price statistics across collection"""
    min_price = db.query(func.min(Bottle.price_paid)).filter(
        Bottle.price_paid != None
    ).scalar()
    
    max_price = db.query(func.max(Bottle.price_paid)).filter(
        Bottle.price_paid != None
    ).scalar()
    
    avg_price = db.query(func.avg(Bottle.price_paid)).filter(
        Bottle.price_paid != None
    ).scalar()
    
    median_price = db.query(Bottle.price_paid).filter(
        Bottle.price_paid != None
    ).order_by(Bottle.price_paid).all()
    
    median = None
    if median_price:
        mid = len(median_price) // 2
        if len(median_price) % 2 == 0:
            median = (median_price[mid - 1][0] + median_price[mid][0]) / 2
        else:
            median = median_price[mid][0]
    
    return {
        "min_price": float(min_price) if min_price else None,
        "max_price": float(max_price) if max_price else None,
        "average_price": float(avg_price) if avg_price else None,
        "median_price": float(median) if median else None,
    }
