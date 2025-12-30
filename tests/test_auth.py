"""Authentication tests"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_register_success():
    """Test successful user registration"""
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword123",
            "display_name": "Test User",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "testuser@example.com"
    assert "password_hash" not in data


def test_register_duplicate_username():
    """Test registration with duplicate username"""
    user_data = {
        "username": "duplicate",
        "email": "user1@example.com",
        "password": "testpassword123",
        "display_name": "User One",
    }
    
    # First registration should succeed
    response1 = client.post("/auth/register", json=user_data)
    assert response1.status_code == 201
    
    # Second registration with same username should fail
    user_data["email"] = "user2@example.com"
    response2 = client.post("/auth/register", json=user_data)
    assert response2.status_code == 409
    assert "Username already registered" in response2.json()["detail"]


def test_register_duplicate_email():
    """Test registration with duplicate email"""
    user_data = {
        "username": "user_one",
        "email": "duplicate@example.com",
        "password": "testpassword123",
        "display_name": "User One",
    }
    
    # First registration should succeed
    response1 = client.post("/auth/register", json=user_data)
    assert response1.status_code == 201
    
    # Second registration with same email should fail
    user_data["username"] = "user_two"
    response2 = client.post("/auth/register", json=user_data)
    assert response2.status_code == 409
    assert "Email already registered" in response2.json()["detail"]


def test_login_success():
    """Test successful user login"""
    # Register user first
    register_data = {
        "username": "logintest",
        "email": "logintest@example.com",
        "password": "testpassword123",
        "display_name": "Login Test",
    }
    client.post("/auth/register", json=register_data)
    
    # Login with correct credentials
    response = client.post(
        "/auth/login",
        params={"username": "logintest", "password": "testpassword123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer"
    assert "access_token" in data
    assert data["user"]["username"] == "logintest"


def test_login_invalid_username():
    """Test login with invalid username"""
    response = client.post(
        "/auth/login",
        params={"username": "nonexistent", "password": "password"},
    )
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]


def test_login_invalid_password():
    """Test login with invalid password"""
    # Register user first
    register_data = {
        "username": "passwordtest",
        "email": "passwordtest@example.com",
        "password": "correctpassword",
        "display_name": "Password Test",
    }
    client.post("/auth/register", json=register_data)
    
    # Login with wrong password
    response = client.post(
        "/auth/login",
        params={"username": "passwordtest", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]


def test_get_user_profile():
    """Test getting user profile"""
    # Register and login user
    register_data = {
        "username": "profiletest",
        "email": "profiletest@example.com",
        "password": "testpassword123",
        "display_name": "Profile Test",
    }
    register_resp = client.post("/auth/register", json=register_data)
    user_id = register_resp.json()["id"]
    
    # Get user profile
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "profiletest"
    assert data["email"] == "profiletest@example.com"


def test_get_nonexistent_user():
    """Test getting non-existent user"""
    response = client.get("/users/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


def test_get_current_user_unauthorized():
    """Test getting current user without authentication"""
    response = client.get("/users/me")
    assert response.status_code == 403
