"""Search and discovery tests"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_search_bottles(auth_token):
    """Test basic bottle search"""
    # Create test bottles
    for name in ["Macallan", "Balvenie", "Dalmore"]:
        client.post(
            "/bottles",
            headers={"Authorization": auth_token},
            json={
                "name": f"{name} 18 Year",
                "spirit_type": "whiskey",
                "distillery": name,
                "research": False,
            },
        )
    
    # Search
    response = client.get("/search/bottles?q=Macallan")
    assert response.status_code == 200
    results = response.json()
    assert len(results) > 0
    assert any("Macallan" in b["name"] for b in results)


def test_search_by_distillery(auth_token):
    """Test searching by distillery"""
    # Create bottle
    client.post(
        "/bottles",
        headers={"Authorization": auth_token},
        json={
            "name": "Highland Park 18",
            "spirit_type": "whiskey",
            "distillery": "Highland Park",
            "research": False,
        },
    )
    
    # Search by distillery
    response = client.get("/search/bottles?q=Highland%20Park")
    assert response.status_code == 200
    results = response.json()
    assert any("Highland Park" in b["distillery"] for b in results)


def test_filter_by_spirit_type(auth_token):
    """Test filtering by spirit type"""
    # Create multiple bottles
    for spirit in ["whiskey", "vodka", "rum"]:
        client.post(
            "/bottles",
            headers={"Authorization": auth_token},
            json={
                "name": f"{spirit.capitalize()} Test",
                "spirit_type": spirit,
                "research": False,
            },
        )
    
    # Filter by spirit type
    response = client.get("/search/filter?spirit_type=whiskey")
    assert response.status_code == 200
    data = response.json()
    assert all(b["spirit_type"] == "whiskey" for b in data["bottles"])


def test_filter_by_proof(auth_token):
    """Test filtering by proof range"""
    # Create bottles with different proofs
    for proof in [80, 100, 120]:
        client.post(
            "/bottles",
            headers={"Authorization": auth_token},
            json={
                "name": f"Bottle {proof}",
                "spirit_type": "whiskey",
                "proof": proof,
                "research": False,
            },
        )
    
    # Filter by proof range
    response = client.get("/search/filter?min_proof=100&max_proof=120")
    assert response.status_code == 200
    data = response.json()
    assert all(b["proof"] >= 100 and b["proof"] <= 120 for b in data["bottles"])


def test_filter_by_rating(auth_token):
    """Test filtering by rating"""
    # Create bottles with different ratings
    for rating in [2, 3, 4, 5]:
        client.post(
            "/bottles",
            headers={"Authorization": auth_token},
            json={
                "name": f"Bottle Rating {rating}",
                "spirit_type": "whiskey",
                "rating": rating,
                "research": False,
            },
        )
    
    # Filter by rating
    response = client.get("/search/filter?min_rating=4&max_rating=5")
    assert response.status_code == 200
    data = response.json()
    assert all(b["rating"] >= 4 for b in data["bottles"])


def test_filter_by_price(auth_token):
    """Test filtering by price range"""
    # Create bottles with different prices
    for price in [50, 75, 100, 150]:
        client.post(
            "/bottles",
            headers={"Authorization": auth_token},
            json={
                "name": f"Bottle ${price}",
                "spirit_type": "whiskey",
                "price_paid": price,
                "research": False,
            },
        )
    
    # Filter by price
    response = client.get("/search/filter?min_price=75&max_price=150")
    assert response.status_code == 200
    data = response.json()
    prices = [b["price_paid"] for b in data["bottles"] if b["price_paid"]]
    assert all(75 <= p <= 150 for p in prices)


def test_filter_by_region(auth_token):
    """Test filtering by region"""
    # Create bottles from different regions
    for region in ["Speyside", "Islay", "Highland"]:
        client.post(
            "/bottles",
            headers={"Authorization": auth_token},
            json={
                "name": f"{region} Whiskey",
                "spirit_type": "whiskey",
                "region": region,
                "research": False,
            },
        )
    
    # Filter by region
    response = client.get("/search/filter?region=Speyside")
    assert response.status_code == 200
    data = response.json()
    assert all("Speyside" in b["region"] for b in data["bottles"] if b["region"])


def test_filter_by_country(auth_token):
    """Test filtering by country"""
    # Create bottles from different countries
    for country in ["Scotland", "Ireland", "USA"]:
        client.post(
            "/bottles",
            headers={"Authorization": auth_token},
            json={
                "name": f"{country} Spirit",
                "spirit_type": "whiskey",
                "country": country,
                "research": False,
            },
        )
    
    # Filter by country
    response = client.get("/search/filter?country=Scotland")
    assert response.status_code == 200
    data = response.json()
    assert all("Scotland" in b["country"] for b in data["bottles"] if b["country"])


def test_filter_sorting(auth_token):
    """Test sorting results"""
    # Create bottles with different ratings
    for i, rating in enumerate([1, 2, 3, 4, 5]):
        client.post(
            "/bottles",
            headers={"Authorization": auth_token},
            json={
                "name": f"Bottle {i}",
                "spirit_type": "whiskey",
                "rating": rating,
                "research": False,
            },
        )
    
    # Sort by rating descending
    response = client.get("/search/filter?sort_by=rating&sort_order=desc")
    assert response.status_code == 200
    data = response.json()
    bottles = data["bottles"]
    ratings = [b["rating"] for b in bottles if b["rating"]]
    # Check descending order
    assert all(ratings[i] >= ratings[i + 1] for i in range(len(ratings) - 1))


def test_filter_pagination(auth_token):
    """Test pagination in results"""
    # Create many bottles
    for i in range(10):
        client.post(
            "/bottles",
            headers={"Authorization": auth_token},
            json={
                "name": f"Bottle {i}",
                "spirit_type": "whiskey",
                "research": False,
            },
        )
    
    # Get first page
    response1 = client.get("/search/filter?skip=0&limit=5")
    assert response1.status_code == 200
    page1 = response1.json()
    assert len(page1["bottles"]) <= 5
    
    # Get second page
    response2 = client.get("/search/filter?skip=5&limit=5")
    page2 = response2.json()
    assert len(page2["bottles"]) <= 5


def test_popular_bottles(auth_token):
    """Test getting popular bottles"""
    response = client.get("/search/popular")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_catalog_stats():
    """Test getting catalog statistics (public)"""
    response = client.get("/search/stats")
    assert response.status_code == 200
    stats = response.json()
    assert "total_bottles" in stats
    assert "spirit_breakdown" in stats
    assert "average_price" in stats
    assert "most_common_spirit" in stats


def test_region_bottles(auth_token):
    """Test getting bottles by region"""
    # Create bottle in region
    client.post(
        "/bottles",
        headers={"Authorization": auth_token},
        json={
            "name": "Speyside Whiskey",
            "spirit_type": "whiskey",
            "region": "Speyside",
            "research": False,
        },
    )
    
    # Get region bottles
    response = client.get("/search/regions/Speyside")
    assert response.status_code == 200
    bottles = response.json()
    assert any("Speyside" in b["region"] for b in bottles)


def test_country_bottles(auth_token):
    """Test getting bottles by country"""
    # Create bottle in country
    client.post(
        "/bottles",
        headers={"Authorization": auth_token},
        json={
            "name": "Scottish Whiskey",
            "spirit_type": "whiskey",
            "country": "Scotland",
            "research": False,
        },
    )
    
    # Get country bottles
    response = client.get("/search/countries/Scotland")
    assert response.status_code == 200
    bottles = response.json()
    assert any("Scotland" in b["country"] for b in bottles)


def test_distillery_profile(auth_token):
    """Test getting distillery profile"""
    # Create bottles from distillery
    for i in range(3):
        client.post(
            "/bottles",
            headers={"Authorization": auth_token},
            json={
                "name": f"Macallan {i}",
                "spirit_type": "whiskey",
                "distillery": "Macallan",
                "region": "Speyside",
                "country": "Scotland",
                "research": False,
            },
        )
    
    # Get distillery profile
    response = client.get("/search/distillery/Macallan")
    assert response.status_code == 200
    profile = response.json()
    assert profile["distillery"] == "Macallan"
    assert profile["total_bottles"] >= 3


def test_pricing_stats(auth_token):
    """Test pricing statistics"""
    # Create bottles with prices
    for price in [50, 75, 100, 150, 200]:
        client.post(
            "/bottles",
            headers={"Authorization": auth_token},
            json={
                "name": f"Bottle ${price}",
                "spirit_type": "whiskey",
                "price_paid": price,
                "research": False,
            },
        )
    
    # Get pricing stats
    response = client.get("/search/pricing/stats")
    assert response.status_code == 200
    stats = response.json()
    assert "min_price" in stats
    assert "max_price" in stats
    assert "average_price" in stats
    assert "median_price" in stats
