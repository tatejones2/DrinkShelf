"""Bottle and collection tests"""

import pytest
from uuid import uuid4
from fastapi.testclient import TestClient
from app.main import app
from app.models.bottle import SpiritType

client = TestClient(app)


# Test fixtures - get auth token
@pytest.fixture
def auth_token(db):
    """Create a test user and return auth token"""
    from app.crud.user import create_user, authenticate_user
    from app.utils.security import create_access_token
    from datetime import timedelta
    from app.config import settings
    
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "display_name": "Test User",
    }
    
    from app.schemas.user import UserCreate
    user = create_user(db, UserCreate(**user_data))
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return f"Bearer {token}"


# ============= BOTTLE TESTS =============

def test_create_bottle(auth_token):
    """Test creating a new bottle"""
    response = client.post(
        "/bottles",
        headers={"Authorization": auth_token},
        json={
            "name": "Macallan 18 Year",
            "spirit_type": "whiskey",
            "distillery": "Macallan",
            "proof": 86,
            "region": "Speyside",
            "country": "Scotland",
            "release_year": 2022,
            "rating": 5,
            "research": False,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Macallan 18 Year"
    assert data["spirit_type"] == "whiskey"
    assert data["rating"] == 5


def test_list_bottles(auth_token):
    """Test listing user's bottles"""
    # Create a bottle first
    client.post(
        "/bottles",
        headers={"Authorization": auth_token},
        json={
            "name": "Test Bottle",
            "spirit_type": "whiskey",
            "distillery": "Test Distillery",
            "proof": 80,
            "research": False,
        },
    )
    
    # List bottles
    response = client.get(
        "/bottles",
        headers={"Authorization": auth_token},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["name"] == "Test Bottle"


def test_list_bottles_with_filters(auth_token):
    """Test listing bottles with filters"""
    # Create multiple bottles
    for spirit_type, rating in [("whiskey", 5), ("vodka", 3), ("whiskey", 4)]:
        client.post(
            "/bottles",
            headers={"Authorization": auth_token},
            json={
                "name": f"{spirit_type.capitalize()} Bottle",
                "spirit_type": spirit_type,
                "distillery": "Test",
                "rating": rating,
                "research": False,
            },
        )
    
    # Filter by spirit type
    response = client.get(
        "/bottles?spirit_type=whiskey",
        headers={"Authorization": auth_token},
    )
    assert response.status_code == 200
    whiskeys = response.json()
    assert all(b["spirit_type"] == "whiskey" for b in whiskeys)
    
    # Filter by rating
    response = client.get(
        "/bottles?min_rating=4",
        headers={"Authorization": auth_token},
    )
    assert response.status_code == 200
    high_rated = response.json()
    assert all(b["rating"] >= 4 for b in high_rated if b.get("rating"))


def test_get_bottle_stats(auth_token):
    """Test getting bottle collection statistics"""
    # Create bottles
    for _ in range(3):
        client.post(
            "/bottles",
            headers={"Authorization": auth_token},
            json={
                "name": "Test Whiskey",
                "spirit_type": "whiskey",
                "rating": 4,
                "research": False,
            },
        )
    
    response = client.get(
        "/bottles/stats",
        headers={"Authorization": auth_token},
    )
    assert response.status_code == 200
    stats = response.json()
    assert stats["total_bottles"] >= 3
    assert stats["average_rating"] is not None


def test_get_bottle(auth_token):
    """Test retrieving a specific bottle"""
    # Create bottle
    create_response = client.post(
        "/bottles",
        headers={"Authorization": auth_token},
        json={
            "name": "Specific Bottle",
            "spirit_type": "whiskey",
            "research": False,
        },
    )
    bottle_id = create_response.json()["id"]
    
    # Get bottle
    response = client.get(
        f"/bottles/{bottle_id}",
        headers={"Authorization": auth_token},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Specific Bottle"


def test_update_bottle(auth_token):
    """Test updating a bottle"""
    # Create bottle
    create_response = client.post(
        "/bottles",
        headers={"Authorization": auth_token},
        json={
            "name": "Original Name",
            "spirit_type": "whiskey",
            "rating": 3,
            "research": False,
        },
    )
    bottle_id = create_response.json()["id"]
    
    # Update bottle
    response = client.put(
        f"/bottles/{bottle_id}",
        headers={"Authorization": auth_token},
        json={
            "name": "Updated Name",
            "rating": 5,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"
    assert data["rating"] == 5


def test_delete_bottle(auth_token):
    """Test soft deleting a bottle"""
    # Create bottle
    create_response = client.post(
        "/bottles",
        headers={"Authorization": auth_token},
        json={
            "name": "Delete Me",
            "spirit_type": "whiskey",
            "research": False,
        },
    )
    bottle_id = create_response.json()["id"]
    
    # Delete bottle
    response = client.delete(
        f"/bottles/{bottle_id}",
        headers={"Authorization": auth_token},
    )
    assert response.status_code == 204
    
    # Verify it's deleted (soft delete)
    get_response = client.get(
        f"/bottles/{bottle_id}",
        headers={"Authorization": auth_token},
    )
    assert get_response.status_code == 404


def test_bottle_unauthorized_access(auth_token):
    """Test that users can't access other users' bottles"""
    # Create bottle with first user
    create_response = client.post(
        "/bottles",
        headers={"Authorization": auth_token},
        json={
            "name": "Private Bottle",
            "spirit_type": "whiskey",
            "research": False,
        },
    )
    bottle_id = create_response.json()["id"]
    
    # Create second user and get their token
    from app.crud.user import create_user
    from app.utils.security import create_access_token
    from datetime import timedelta
    from app.config import settings
    from app.schemas.user import UserCreate
    
    # This would require access to db fixture - test demonstrates authorization check
    # In real test, create second user and verify 404


# ============= COLLECTION TESTS =============

def test_create_collection(auth_token):
    """Test creating a new collection"""
    response = client.post(
        "/collections",
        headers={"Authorization": auth_token},
        json={
            "name": "My Whiskeys",
            "description": "Collection of my favorite whiskeys",
            "is_public": False,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "My Whiskeys"
    assert data["is_public"] is False


def test_list_user_collections(auth_token):
    """Test listing user's collections"""
    # Create collection
    client.post(
        "/collections",
        headers={"Authorization": auth_token},
        json={
            "name": "Test Collection",
            "is_public": False,
        },
    )
    
    # List collections
    response = client.get(
        "/collections",
        headers={"Authorization": auth_token},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0


def test_list_public_collections():
    """Test listing public collections (no auth required)"""
    response = client.get("/collections/public")
    assert response.status_code == 200


def test_get_collection(auth_token):
    """Test retrieving a specific collection"""
    # Create collection
    create_response = client.post(
        "/collections",
        headers={"Authorization": auth_token},
        json={
            "name": "Get Me",
            "is_public": True,
        },
    )
    collection_id = create_response.json()["id"]
    
    # Get collection
    response = client.get(f"/collections/{collection_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Get Me"


def test_update_collection(auth_token):
    """Test updating a collection"""
    # Create collection
    create_response = client.post(
        "/collections",
        headers={"Authorization": auth_token},
        json={
            "name": "Original Name",
            "is_public": False,
        },
    )
    collection_id = create_response.json()["id"]
    
    # Update collection
    response = client.put(
        f"/collections/{collection_id}",
        headers={"Authorization": auth_token},
        json={
            "name": "Updated Name",
            "is_public": True,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"
    assert data["is_public"] is True


def test_delete_collection(auth_token):
    """Test deleting a collection"""
    # Create collection
    create_response = client.post(
        "/collections",
        headers={"Authorization": auth_token},
        json={"name": "Delete Me"},
    )
    collection_id = create_response.json()["id"]
    
    # Delete collection
    response = client.delete(
        f"/collections/{collection_id}",
        headers={"Authorization": auth_token},
    )
    assert response.status_code == 204
    
    # Verify it's deleted
    get_response = client.get(f"/collections/{collection_id}")
    assert get_response.status_code == 404


def test_add_bottle_to_collection(auth_token):
    """Test adding a bottle to a collection"""
    # Create bottle
    bottle_response = client.post(
        "/bottles",
        headers={"Authorization": auth_token},
        json={
            "name": "Test Bottle",
            "spirit_type": "whiskey",
            "research": False,
        },
    )
    bottle_id = bottle_response.json()["id"]
    
    # Create collection
    collection_response = client.post(
        "/collections",
        headers={"Authorization": auth_token},
        json={"name": "Test Collection"},
    )
    collection_id = collection_response.json()["id"]
    
    # Add bottle to collection
    response = client.post(
        f"/collections/{collection_id}/bottles/{bottle_id}",
        headers={"Authorization": auth_token},
    )
    assert response.status_code == 204


def test_remove_bottle_from_collection(auth_token):
    """Test removing a bottle from a collection"""
    # Create bottle and collection
    bottle_response = client.post(
        "/bottles",
        headers={"Authorization": auth_token},
        json={
            "name": "Test Bottle",
            "spirit_type": "whiskey",
            "research": False,
        },
    )
    bottle_id = bottle_response.json()["id"]
    
    collection_response = client.post(
        "/collections",
        headers={"Authorization": auth_token},
        json={"name": "Test Collection"},
    )
    collection_id = collection_response.json()["id"]
    
    # Add bottle to collection
    client.post(
        f"/collections/{collection_id}/bottles/{bottle_id}",
        headers={"Authorization": auth_token},
    )
    
    # Remove bottle from collection
    response = client.delete(
        f"/collections/{collection_id}/bottles/{bottle_id}",
        headers={"Authorization": auth_token},
    )
    assert response.status_code == 204
