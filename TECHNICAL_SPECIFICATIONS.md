# DrinkShelf - Technical Specifications

## Backend Structure

### Project Directory Layout
```
drinkshelf-backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── dependencies.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── bottle.py
│   │   ├── collection.py
│   │   ├── tasting_note.py
│   │   └── base.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── bottle.py
│   │   ├── collection.py
│   │   └── tasting_note.py
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── bottle.py
│   │   ├── collection.py
│   │   └── tasting_note.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── router.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── auth.py
│   │       ├── users.py
│   │       ├── bottles.py
│   │       ├── collections.py
│   │       ├── search.py
│   │       ├── ai.py
│   │       └── tasting_notes.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ai_service.py
│   │   ├── bottle_classifier.py
│   │   └── search_service.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── security.py
│   │   ├── validators.py
│   │   └── constants.py
│   └── database/
│       ├── __init__.py
│       ├── session.py
│       └── base.py
├── migrations/
│   └── versions/
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_bottles.py
│   ├── test_collections.py
│   ├── test_ai_service.py
│   └── test_search.py
├── .env.example
├── .gitignore
├── requirements.txt
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
└── README.md
```

---

## Database Relationships Diagram

```
Users (1) ──────────────→ (∞) Bottles
  │                          │
  │                          ├─→ (∞) TastingNotes
  │                          └─→ (∞) CollectionBottles → Collections
  │
  └─────────────────────→ (∞) Collections
                            │
                            └─→ (∞) CollectionBottles → Bottles

```

---

## Core Data Models

### User Model
```python
class User(Base):
    __tablename__ = "users"
    
    id: UUID4 = Column(UUID, primary_key=True, default=uuid4)
    username: str = Column(String(50), unique=True, index=True)
    email: str = Column(String(255), unique=True, index=True)
    password_hash: str = Column(String(255))
    display_name: str = Column(String(100), nullable=True)
    bio: str = Column(Text, nullable=True)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    bottles: relationship = relationship("Bottle", back_populates="user")
    collections: relationship = relationship("Collection", back_populates="user")
    tasting_notes: relationship = relationship("TastingNote", back_populates="user")
```

### Bottle Model
```python
class SpiritType(str, Enum):
    WHISKEY = "whiskey"
    VODKA = "vodka"
    TEQUILA = "tequila"
    RUM = "rum"
    GIN = "gin"
    BEER = "beer"
    WINE = "wine"
    LIQUEUR = "liqueur"
    OTHER = "other"

class Bottle(Base):
    __tablename__ = "bottles"
    
    id: UUID4 = Column(UUID, primary_key=True, default=uuid4)
    user_id: UUID4 = Column(UUID, ForeignKey("users.id"), nullable=False, index=True)
    name: str = Column(String(255), nullable=False, index=True)
    spirit_type: SpiritType = Column(Enum(SpiritType), nullable=False, index=True)
    distillery: str = Column(String(255), nullable=True, index=True)
    proof: float = Column(Float, nullable=True)
    age_statement: str = Column(String(50), nullable=True)
    region: str = Column(String(100), nullable=True)
    country: str = Column(String(100), nullable=True, index=True)
    release_year: int = Column(Integer, nullable=True)
    batch_number: str = Column(String(100), nullable=True)
    price_paid: Decimal = Column(Numeric(10, 2), nullable=True)
    price_current: Decimal = Column(Numeric(10, 2), nullable=True)
    acquisition_date: date = Column(Date, nullable=True)
    notes: str = Column(Text, nullable=True)
    rating: int = Column(Integer, nullable=True)  # 1-5
    image_url: str = Column(String(500), nullable=True)
    ai_details: dict = Column(JSON, nullable=True)
    created_at: datetime = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at: datetime = Column(DateTime, nullable=True, index=True)
    
    user: relationship = relationship("User", back_populates="bottles")
    tasting_notes: relationship = relationship("TastingNote", back_populates="bottle")
    collections: relationship = relationship("Collection", secondary="collection_bottles", back_populates="bottles")
```

### Collection Model
```python
class Collection(Base):
    __tablename__ = "collections"
    
    id: UUID4 = Column(UUID, primary_key=True, default=uuid4)
    user_id: UUID4 = Column(UUID, ForeignKey("users.id"), nullable=False, index=True)
    name: str = Column(String(255), nullable=False)
    description: str = Column(Text, nullable=True)
    is_public: bool = Column(Boolean, default=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user: relationship = relationship("User", back_populates="collections")
    bottles: relationship = relationship("Bottle", secondary="collection_bottles", back_populates="collections")
```

### TastingNote Model
```python
class TastingNote(Base):
    __tablename__ = "tasting_notes"
    
    id: UUID4 = Column(UUID, primary_key=True, default=uuid4)
    bottle_id: UUID4 = Column(UUID, ForeignKey("bottles.id"), nullable=False, index=True)
    user_id: UUID4 = Column(UUID, ForeignKey("users.id"), nullable=False, index=True)
    nose: str = Column(Text, nullable=True)
    palate: str = Column(Text, nullable=True)
    finish: str = Column(Text, nullable=True)
    overall_notes: str = Column(Text, nullable=True)
    rating: int = Column(Integer, nullable=True)  # 1-5
    tasted_date: date = Column(Date, nullable=True)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    bottle: relationship = relationship("Bottle", back_populates="tasting_notes")
    user: relationship = relationship("User", back_populates="tasting_notes")
```

---

## API Request/Response Examples

### Add Bottle with AI Research
**Request:**
```json
POST /bottles
{
  "name": "1792 Small Batch Bourbon",
  "research": true
}
```

**Response:**
```json
{
  "id": "uuid-here",
  "name": "1792 Small Batch Bourbon",
  "spirit_type": "whiskey",
  "distillery": "Barton 1792 Distillery",
  "proof": 100,
  "age_statement": "No age statement",
  "region": "Kentucky",
  "country": "United States",
  "release_year": null,
  "batch_number": null,
  "price_paid": null,
  "price_current": 25.99,
  "acquisition_date": null,
  "notes": "Accessible bourbon with balanced oak and vanilla notes",
  "rating": null,
  "image_url": null,
  "ai_details": {
    "key_characteristics": ["Caramel", "Vanilla", "Oak"],
    "price_range": "$25-35",
    "availability": "Widely available",
    "production_notes": "Aged in new charred oak barrels"
  },
  "created_at": "2025-01-01T12:00:00Z",
  "updated_at": "2025-01-01T12:00:00Z"
}
```

### Search Bottles
**Request:**
```
GET /search?query=bourbon&spirit_type=whiskey&proof_min=80&proof_max=120&page=1&limit=20
```

**Response:**
```json
{
  "items": [
    {
      "id": "uuid-1",
      "name": "1792 Small Batch Bourbon",
      "spirit_type": "whiskey",
      "proof": 100,
      "distillery": "Barton 1792 Distillery",
      "rating": 4.2,
      "image_url": "url-here"
    }
  ],
  "total": 45,
  "page": 1,
  "limit": 20,
  "pages": 3
}
```

### User Statistics
**Request:**
```
GET /users/{user_id}/statistics
```

**Response:**
```json
{
  "total_bottles": 127,
  "bottles_by_type": {
    "whiskey": 65,
    "vodka": 12,
    "tequila": 8,
    "rum": 15,
    "other": 27
  },
  "average_rating": 4.1,
  "highest_proof": 151,
  "lowest_proof": 35,
  "total_estimated_value": 4250.75,
  "collections_count": 5,
  "countries_represented": 12,
  "distilleries_count": 89
}
```

---

## Authentication Flow

1. User registers with email and password
2. Password is hashed using bcrypt
3. JWT token issued on login
4. Token included in Authorization header: `Bearer {token}`
5. Token expires after 24 hours (configurable)
6. Refresh token endpoint for extending session

---

## Error Handling

All endpoints follow standard HTTP status codes:
- `200 OK` - Successful GET/PUT
- `201 Created` - Successful POST
- `204 No Content` - Successful DELETE
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Missing/invalid authentication
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `409 Conflict` - Resource already exists (e.g., duplicate username)
- `422 Unprocessable Entity` - Validation errors
- `500 Internal Server Error` - Server error

### Error Response Format
```json
{
  "detail": "Error message here",
  "code": "ERROR_CODE",
  "timestamp": "2025-01-01T12:00:00Z"
}
```

---

## OpenAI Integration Details

### Service Configuration
- Model: GPT-4 (or GPT-3.5-turbo for cost optimization)
- Max tokens: 500
- Temperature: 0.3 (for consistent, factual responses)
- Timeout: 30 seconds

### Bottle Research Prompt
```
You are an expert sommelier and spirits connoisseur. Provide accurate, detailed information 
about the following spirit:

{bottle_name}

Return ONLY valid JSON with these exact fields:
{
  "spirit_type": "whiskey|vodka|tequila|rum|gin|beer|wine|liqueur|other",
  "distillery": "...",
  "proof": number or null,
  "age_statement": "...",
  "region": "...",
  "country": "...",
  "production_notes": "...",
  "tasting_profile": ["...", "..."],
  "price_range": "...",
  "availability": "common|limited|rare",
  "awards": ["..."]
}

Ensure all information is accurate. Return null for unknown fields.
```

### Response Caching
- Store AI responses for 90 days
- Use bottle name + distillery as cache key
- Reduce OpenAI API costs and improve response time

---

## Rate Limiting
- Authentication endpoints: 5 requests per minute per IP
- General API: 100 requests per minute per authenticated user
- AI research: 10 requests per minute per user

---

## Pagination Standard
- Default limit: 20 items
- Maximum limit: 100 items
- Use cursor-based pagination for large datasets if needed

---

## Database Indexing Strategy
```sql
-- Performance-critical indexes
CREATE INDEX idx_bottles_user_id ON bottles(user_id);
CREATE INDEX idx_bottles_spirit_type ON bottles(spirit_type);
CREATE INDEX idx_bottles_distillery ON bottles(distillery);
CREATE INDEX idx_bottles_country ON bottles(country);
CREATE INDEX idx_bottles_created_at ON bottles(created_at);
CREATE INDEX idx_bottles_deleted_at ON bottles(deleted_at);

CREATE INDEX idx_collections_user_id ON collections(user_id);
CREATE INDEX idx_tasting_notes_bottle_id ON tasting_notes(bottle_id);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);

-- Composite indexes
CREATE INDEX idx_bottles_user_type ON bottles(user_id, spirit_type);
CREATE INDEX idx_bottles_search ON bottles(user_id, distillery, spirit_type) WHERE deleted_at IS NULL;
```
