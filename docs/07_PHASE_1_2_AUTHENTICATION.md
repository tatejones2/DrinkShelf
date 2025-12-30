# Phase 1.2: Authentication System Implementation

## Overview

Phase 1.2 has been successfully completed, implementing a complete authentication system for the DrinkShelf backend using FastAPI and JWT tokens.

## Features Implemented

### 1. User Registration (`POST /auth/register`)
- Create new user accounts with email and username validation
- Automatic password hashing using bcrypt
- Duplicate username/email prevention
- Returns user profile with auto-generated UUID

**Request:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password_123",
  "display_name": "John Doe"
}
```

**Response (201 Created):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "username": "john_doe",
  "email": "john@example.com",
  "display_name": "John Doe",
  "bio": null,
  "created_at": "2024-12-30T15:30:00Z",
  "updated_at": "2024-12-30T15:30:00Z"
}
```

### 2. User Login (`POST /auth/login`)
- Authenticate with username and password
- Generate JWT access token with configurable expiration
- Return user profile with token

**Request:**
```
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=john_doe&password=secure_password_123
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "username": "john_doe",
    "email": "john@example.com",
    "display_name": "John Doe"
  }
}
```

### 3. Protected Routes

All routes requiring authentication use the `get_current_user` dependency:

- **GET /users/me** - Get current authenticated user's profile
- **PUT /users/{user_id}** - Update user profile (only own profile)

**Usage (include JWT token):**
```
GET /users/me
Authorization: Bearer <access_token>
```

### 4. User Profiles

- **GET /users/{user_id}** - Get public user profile (no auth required)
- **PUT /users/{user_id}** - Update own profile (requires auth)

## Technical Architecture

### Security Components

#### Password Hashing (`app/utils/security.py`)
- **Algorithm**: bcrypt with salt rounds = 12
- **Functions**:
  - `get_password_hash(password: str) -> str` - Hash password for storage
  - `verify_password(plain_password: str, hashed_password: str) -> bool` - Verify password

#### JWT Token Management (`app/utils/security.py`)
- **Algorithm**: HS256 (HMAC-SHA256)
- **Expiration**: Configurable via `ACCESS_TOKEN_EXPIRE_MINUTES` (default: 30 minutes)
- **Payload**: `{"sub": user_id, "exp": expiration_timestamp}`
- **Functions**:
  - `create_access_token(data: dict, expires_delta: timedelta) -> str` - Generate token
  - `decode_token(token: str) -> dict | None` - Validate and decode token

### Database Models

#### User Model (`app/models/user.py`)
```python
class User(Base):
    __tablename__ = "users"
    
    id: UUID = Column(UUID, primary_key=True, default=uuid4)
    username: str = Column(String(50), unique=True, index=True, nullable=False)
    email: str = Column(String(255), unique=True, index=True, nullable=False)
    password_hash: str = Column(String(255), nullable=False)
    display_name: str = Column(String(255))
    bio: str = Column(Text, nullable=True)
    created_at: datetime = Column(DateTime, server_default=func.now())
    updated_at: datetime = Column(DateTime, server_default=func.now(), onupdate=func.now())
```

### API Routes

#### Authentication Routes (`app/api/routes/auth.py`)
- `POST /auth/register` - User registration
- `POST /auth/login` - User login with JWT token generation

#### User Routes (`app/api/routes/users.py`)
- `GET /users/{user_id}` - Get user profile by ID
- `GET /users/me` - Get current authenticated user
- `PUT /users/{user_id}` - Update user profile

### CRUD Operations (`app/crud/user.py`)
- `create_user()` - Create new user with password hashing
- `get_user_by_id()` - Retrieve user by UUID
- `get_user_by_username()` - Retrieve user by username
- `get_user_by_email()` - Retrieve user by email
- `authenticate_user()` - Verify credentials
- `update_user()` - Update user profile

### Dependencies (`app/dependencies.py`)
- `get_current_user()` - Dependency that validates JWT token and returns authenticated user

## Pydantic Schemas

### UserCreate
```python
class UserCreate(BaseModel):
    username: str  # 3-50 characters, alphanumeric + underscore
    email: str     # Valid email format
    password: str  # 8+ characters
    display_name: str
```

### UserRead
```python
class UserRead(BaseModel):
    id: UUID
    username: str
    email: str
    display_name: str
    bio: Optional[str]
    created_at: datetime
    updated_at: datetime
```

### UserUpdate
```python
class UserUpdate(BaseModel):
    email: Optional[str] = None
    display_name: Optional[str] = None
    bio: Optional[str] = None
```

## Error Handling

### Registration Errors
- **409 Conflict**: Username or email already registered
  ```json
  {"detail": "Username already registered"}
  ```
  
- **422 Unprocessable Entity**: Validation errors
  ```json
  {"detail": [{"loc": ["body", "username"], "msg": "ensure this value has at most 50 characters"}]}
  ```

### Login Errors
- **401 Unauthorized**: Invalid credentials
  ```json
  {"detail": "Incorrect username or password"}
  ```

### Protected Route Errors
- **401 Unauthorized**: Missing or invalid token
  ```json
  {"detail": "Invalid authentication credentials"}
  ```
  
- **403 Forbidden**: Insufficient permissions
  ```json
  {"detail": "Cannot update other users' profiles"}
  ```

## Configuration

Environment variables in `.env`:
```env
# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database
DATABASE_URL=postgresql://user:password@localhost/drinkshelf

# CORS
CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]
```

## Testing

Comprehensive test suite in `tests/test_auth.py`:

- ✅ `test_register_success()` - Successful user registration
- ✅ `test_register_duplicate_username()` - Duplicate username error
- ✅ `test_register_duplicate_email()` - Duplicate email error
- ✅ `test_login_success()` - Successful login with token
- ✅ `test_login_invalid_username()` - Invalid username error
- ✅ `test_login_invalid_password()` - Invalid password error
- ✅ `test_get_user_profile()` - Retrieve user profile
- ✅ `test_get_nonexistent_user()` - Non-existent user error
- ✅ `test_get_current_user_unauthorized()` - Unauthorized access error

**Run tests:**
```bash
pytest tests/test_auth.py -v
```

## Security Best Practices

1. **Password Storage**: Passwords are hashed using bcrypt (12 rounds) and never stored in plaintext
2. **JWT Tokens**: 
   - Signed with secret key to prevent tampering
   - Include expiration time to limit token lifetime
   - Use HTTPS in production to prevent token interception
3. **Authorization**: 
   - Users can only update their own profiles
   - Protected routes require valid JWT token
4. **Input Validation**:
   - Email validation using Pydantic
   - Username constraints (alphanumeric + underscore)
   - Password minimum length requirements

## Next Steps - Phase 1.3

The next phase will implement bottle collection management:

1. **Bottle CRUD Operations** (`app/crud/bottle.py`)
   - Create, read, update, delete bottles
   - Soft delete functionality
   - User ownership validation

2. **Bottle Routes** (`app/api/routes/bottles.py`)
   - `POST /bottles` - Create new bottle entry
   - `GET /bottles` - List user's bottles with pagination/filtering
   - `GET /bottles/{bottle_id}` - Get specific bottle details
   - `PUT /bottles/{bottle_id}` - Update bottle information
   - `DELETE /bottles/{bottle_id}` - Soft delete bottle

3. **AI Integration** (`app/services/ai_service.py`)
   - OpenAI integration for bottle research
   - Populate `ai_details` field with automatically fetched information
   - Support for optional research trigger during bottle creation

4. **Bottle Tests** (`tests/test_bottles.py`)
   - CRUD operation tests
   - Authorization tests
   - Soft delete verification
   - AI research trigger tests

## Files Created/Modified in Phase 1.2

### New Files
- `app/crud/__init__.py` - User CRUD operations (duplicated for clarity)
- `app/crud/user.py` - User CRUD operations implementation
- `app/api/routes/auth.py` - Authentication routes (register, login)
- `app/api/routes/users.py` - User profile routes
- `app/dependencies.py` - JWT authentication dependency
- `tests/test_auth.py` - Authentication test suite

### Modified Files
- `app/main.py` - Include auth and user routers
- `app/database/__init__.py` - Export get_db for route imports
- `app/schemas/bottle.py` - Fix Pydantic v2 decimal field compatibility

## Verification

Run the following to verify the authentication system is working:

```bash
# Verify imports
python -c "from app.main import app; print('✓ App imports successfully')"

# Run authentication tests
pytest tests/test_auth.py -v

# Start development server (requires PostgreSQL)
uvicorn app.main:app --reload

# Test endpoints with curl
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","password":"testpass123","display_name":"Test User"}'
```

## Summary

✅ **Phase 1.2 Complete**

- Authentication system fully implemented and tested
- JWT token generation and validation working
- User registration and login operational
- Protected routes with authorization
- Comprehensive test coverage
- All changes committed and pushed to GitHub

The backend now has a secure foundation for user management and can move forward with bottle collection features in Phase 1.3.
