"""Review and rating aggregation service"""

from typing import Optional, List, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.bottle import Bottle
from app.models.tasting_note import TastingNote
from app.models.user import User


async def get_bottle_review_summary(
    db: Session,
    bottle_id: UUID,
) -> Dict[str, Any]:
    """Get comprehensive review summary for a bottle"""
    from app.crud.tasting_note import (
        get_bottle_average_rating,
        get_bottle_tasting_note_count,
    )
    
    avg_rating = await get_bottle_average_rating(db, bottle_id)
    note_count = await get_bottle_tasting_note_count(db, bottle_id)
    
    # Get rating distribution
    rating_dist = db.query(
        TastingNote.rating,
        func.count(TastingNote.id).label("count")
    ).filter(
        TastingNote.bottle_id == bottle_id,
        TastingNote.rating != None,
    ).group_by(TastingNote.rating).all()
    
    rating_distribution = {
        i: next((count for rating, count in rating_dist if rating == i), 0)
        for i in range(1, 6)
    }
    
    # Get top tasting notes (highest rated)
    top_notes = db.query(TastingNote).filter(
        TastingNote.bottle_id == bottle_id,
        TastingNote.rating != None,
    ).order_by(TastingNote.rating.desc()).limit(3).all()
    
    return {
        "bottle_id": bottle_id,
        "average_rating": avg_rating,
        "total_ratings": note_count,
        "rating_distribution": rating_distribution,
        "top_tasting_notes": [
            {
                "id": note.id,
                "user_id": note.user_id,
                "nose": note.nose,
                "palate": note.palate,
                "finish": note.finish,
                "rating": note.rating,
                "created_at": note.created_at,
            }
            for note in top_notes
        ],
    }


async def get_user_flavor_profile(
    db: Session,
    user_id: UUID,
) -> Dict[str, Any]:
    """Get user's flavor preferences based on their tasting notes"""
    # Get user's average rating
    avg_rating = db.query(func.avg(TastingNote.rating)).filter(
        TastingNote.user_id == user_id,
        TastingNote.rating != None,
    ).scalar()
    
    # Most tasted spirits
    most_tasted = db.query(
        Bottle.spirit_type,
        func.count(TastingNote.id).label("count"),
        func.avg(TastingNote.rating).label("avg_rating"),
    ).join(
        Bottle, TastingNote.bottle_id == Bottle.id
    ).filter(
        TastingNote.user_id == user_id,
        TastingNote.rating != None,
    ).group_by(Bottle.spirit_type).order_by(
        func.count(TastingNote.id).desc()
    ).limit(5).all()
    
    # Most mentioned tasting descriptors (simple analysis of common words)
    all_notes = db.query(TastingNote).filter(
        TastingNote.user_id == user_id
    ).all()
    
    common_descriptors = {}
    descriptors = [
        "sweet", "smooth", "spicy", "fruity", "oaky", "vanilla", "caramel",
        "warm", "dry", "floral", "herbal", "smoky", "peppery", "citrus",
    ]
    
    for note in all_notes:
        text = f"{note.nose} {note.palate} {note.finish}".lower()
        for descriptor in descriptors:
            if descriptor in text:
                common_descriptors[descriptor] = common_descriptors.get(descriptor, 0) + 1
    
    # Sort by frequency
    top_descriptors = sorted(
        common_descriptors.items(),
        key=lambda x: x[1],
        reverse=True
    )[:5]
    
    return {
        "user_id": user_id,
        "average_rating": float(avg_rating) if avg_rating else None,
        "most_tasted_spirits": [
            {
                "spirit_type": str(spirit),
                "count": count,
                "average_rating": float(avg_rating) if avg_rating else None,
            }
            for spirit, count, avg_rating in most_tasted
        ],
        "flavor_preferences": [
            {"descriptor": desc, "frequency": count}
            for desc, count in top_descriptors
        ],
    }


async def get_similar_bottles(
    db: Session,
    bottle_id: UUID,
    limit: int = 5,
) -> List[Dict[str, Any]]:
    """Get bottles similar to the given bottle based on spirit type and ratings"""
    # Get the original bottle
    bottle = db.query(Bottle).filter(Bottle.id == bottle_id).first()
    if not bottle:
        return []
    
    # Find bottles with same spirit type and similar rating
    similar = db.query(Bottle).filter(
        Bottle.spirit_type == bottle.spirit_type,
        Bottle.id != bottle_id,
        Bottle.deleted_at == None,
    ).order_by(Bottle.created_at.desc()).limit(limit).all()
    
    return [
        {
            "id": b.id,
            "name": b.name,
            "spirit_type": b.spirit_type,
            "distillery": b.distillery,
            "rating": b.rating,
        }
        for b in similar
    ]


async def get_recommended_bottles(
    db: Session,
    user_id: UUID,
    limit: int = 10,
) -> List[Dict[str, Any]]:
    """Get bottle recommendations for user based on their tasting preferences"""
    # Get user's preferred spirit types
    user_tasted = db.query(Bottle.spirit_type).distinct().join(
        TastingNote, TastingNote.bottle_id == Bottle.id
    ).filter(
        TastingNote.user_id == user_id
    ).all()
    
    preferred_spirits = [spirit[0] for spirit in user_tasted]
    
    if not preferred_spirits:
        # If no tasting history, recommend highly-rated bottles
        recommendations = db.query(Bottle).filter(
            Bottle.deleted_at == None,
            Bottle.rating >= 4,
        ).order_by(Bottle.rating.desc()).limit(limit).all()
    else:
        # Recommend bottles of preferred spirits with high ratings
        recommendations = db.query(Bottle).filter(
            Bottle.spirit_type.in_(preferred_spirits),
            Bottle.deleted_at == None,
            Bottle.rating >= 3,
        ).order_by(Bottle.rating.desc()).limit(limit).all()
    
    return [
        {
            "id": b.id,
            "name": b.name,
            "spirit_type": b.spirit_type,
            "distillery": b.distillery,
            "rating": b.rating,
        }
        for b in recommendations
    ]
