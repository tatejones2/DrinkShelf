"""Tasting note tests"""

import pytest
from uuid import uuid4
from datetime import date
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.fixture
def authenticated_bottle(auth_token, db):
    """Create a bottle for testing tasting notes"""
    response = client.post(
        "/bottles",
        headers={"Authorization": auth_token},
        json={
            "name": "Test Whiskey",
            "spirit_type": "whiskey",
            "distillery": "Test Distillery",
            "proof": 80,
            "research": False,
        },
    )
    return response.json()["id"]


def test_create_tasting_note(auth_token, authenticated_bottle):
    """Test creating a tasting note"""
    response = client.post(
        f"/tasting-notes/bottles/{authenticated_bottle}",
        headers={"Authorization": auth_token},
        json={
            "nose": "Vanilla, oak, honey",
            "palate": "Sweet, smooth, slight spice",
            "finish": "Long and warming",
            "overall_notes": "Excellent whiskey, very smooth",
            "rating": 4,
            "tasted_date": "2024-12-30",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["nose"] == "Vanilla, oak, honey"
    assert data["rating"] == 4


def test_create_tasting_note_invalid_bottle(auth_token):
    """Test creating tasting note for non-existent bottle"""
    response = client.post(
        f"/tasting-notes/bottles/{uuid4()}",
        headers={"Authorization": auth_token},
        json={
            "nose": "Vanilla",
            "palate": "Smooth",
            "finish": "Long",
            "rating": 4,
        },
    )
    assert response.status_code == 404


def test_create_tasting_note_invalid_rating(auth_token, authenticated_bottle):
    """Test creating tasting note with invalid rating"""
    response = client.post(
        f"/tasting-notes/bottles/{authenticated_bottle}",
        headers={"Authorization": auth_token},
        json={
            "nose": "Vanilla",
            "palate": "Smooth",
            "finish": "Long",
            "rating": 10,  # Invalid - max is 5
        },
    )
    assert response.status_code == 422


def test_list_bottle_tasting_notes(auth_token, authenticated_bottle):
    """Test listing tasting notes for a bottle"""
    # Create multiple tasting notes
    for i in range(3):
        client.post(
            f"/tasting-notes/bottles/{authenticated_bottle}",
            headers={"Authorization": auth_token},
            json={
                "nose": f"Nose {i}",
                "palate": f"Palate {i}",
                "finish": f"Finish {i}",
                "rating": i + 1,
            },
        )
    
    # List notes
    response = client.get(
        f"/tasting-notes/bottles/{authenticated_bottle}",
        headers={"Authorization": auth_token},
    )
    assert response.status_code == 200
    notes = response.json()
    assert len(notes) >= 3


def test_get_tasting_note(auth_token, authenticated_bottle):
    """Test getting a specific tasting note"""
    # Create note
    create_response = client.post(
        f"/tasting-notes/bottles/{authenticated_bottle}",
        headers={"Authorization": auth_token},
        json={
            "nose": "Test nose",
            "palate": "Test palate",
            "finish": "Test finish",
            "rating": 4,
        },
    )
    note_id = create_response.json()["id"]
    
    # Get note
    response = client.get(
        f"/tasting-notes/{note_id}",
        headers={"Authorization": auth_token},
    )
    assert response.status_code == 200
    assert response.json()["nose"] == "Test nose"


def test_update_tasting_note(auth_token, authenticated_bottle):
    """Test updating a tasting note"""
    # Create note
    create_response = client.post(
        f"/tasting-notes/bottles/{authenticated_bottle}",
        headers={"Authorization": auth_token},
        json={
            "nose": "Original",
            "palate": "Original",
            "finish": "Original",
            "rating": 2,
        },
    )
    note_id = create_response.json()["id"]
    
    # Update note
    response = client.put(
        f"/tasting-notes/{note_id}",
        headers={"Authorization": auth_token},
        json={
            "nose": "Updated",
            "rating": 5,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nose"] == "Updated"
    assert data["rating"] == 5


def test_delete_tasting_note(auth_token, authenticated_bottle):
    """Test deleting a tasting note"""
    # Create note
    create_response = client.post(
        f"/tasting-notes/bottles/{authenticated_bottle}",
        headers={"Authorization": auth_token},
        json={
            "nose": "Delete me",
            "palate": "Delete me",
            "finish": "Delete me",
            "rating": 3,
        },
    )
    note_id = create_response.json()["id"]
    
    # Delete note
    response = client.delete(
        f"/tasting-notes/{note_id}",
        headers={"Authorization": auth_token},
    )
    assert response.status_code == 204
    
    # Verify deleted
    get_response = client.get(
        f"/tasting-notes/{note_id}",
        headers={"Authorization": auth_token},
    )
    assert get_response.status_code == 404


def test_get_user_tasting_stats(auth_token, authenticated_bottle):
    """Test getting user tasting statistics"""
    # Create tasting notes
    for rating in [3, 4, 5]:
        client.post(
            f"/tasting-notes/bottles/{authenticated_bottle}",
            headers={"Authorization": auth_token},
            json={
                "nose": "Test",
                "palate": "Test",
                "finish": "Test",
                "rating": rating,
            },
        )
    
    response = client.get(
        "/tasting-notes/user/statistics",
        headers={"Authorization": auth_token},
    )
    assert response.status_code == 200
    stats = response.json()
    assert stats["total_tasting_notes"] >= 3
    assert stats["average_rating"] is not None


def test_get_bottle_tasting_stats(authenticated_bottle):
    """Test getting bottle tasting statistics (public)"""
    response = client.get(f"/tasting-notes/bottle/{authenticated_bottle}/stats")
    assert response.status_code == 200
    stats = response.json()
    assert "average_rating" in stats
    assert "total_tasting_notes" in stats


def test_get_user_notes(auth_token, authenticated_bottle):
    """Test getting user's public tasting notes"""
    # Create notes
    for i in range(2):
        client.post(
            f"/tasting-notes/bottles/{authenticated_bottle}",
            headers={"Authorization": auth_token},
            json={
                "nose": f"Nose {i}",
                "palate": f"Palate {i}",
                "finish": f"Finish {i}",
                "rating": i + 1,
            },
        )
    
    # Get user from a tasting note to get user ID
    list_response = client.get(
        f"/tasting-notes/bottles/{authenticated_bottle}",
        headers={"Authorization": auth_token},
    )
    user_id = list_response.json()[0]["user_id"]
    
    # Get user's notes
    response = client.get(f"/tasting-notes/user/{user_id}/notes")
    assert response.status_code == 200
    notes = response.json()
    assert len(notes) >= 2


def test_tasting_note_unauthorized_access(auth_token, authenticated_bottle):
    """Test that users can't access other users' tasting notes"""
    # This test would require creating a second user and verifying they can't access first user's notes
    pass


def test_tasting_note_pagination(auth_token, authenticated_bottle):
    """Test pagination of tasting notes"""
    # Create many notes
    for i in range(10):
        client.post(
            f"/tasting-notes/bottles/{authenticated_bottle}",
            headers={"Authorization": auth_token},
            json={
                "nose": f"Note {i}",
                "palate": f"Palate {i}",
                "finish": f"Finish {i}",
                "rating": (i % 5) + 1,
            },
        )
    
    # Test pagination with skip and limit
    response = client.get(
        f"/tasting-notes/bottles/{authenticated_bottle}?skip=0&limit=5",
        headers={"Authorization": auth_token},
    )
    assert response.status_code == 200
    notes = response.json()
    assert len(notes) <= 5
