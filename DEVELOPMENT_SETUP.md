# DrinkShelf - Development Setup & Getting Started

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.9+** ([Download](https://www.python.org/downloads/))
- **PostgreSQL 13+** ([Download](https://www.postgresql.org/download/))
- **Git** ([Download](https://git-scm.com/downloads))
- **Docker & Docker Compose** (Optional but recommended) ([Download](https://www.docker.com/products/docker-desktop))
- **pip** or **poetry** (Python package manager - comes with Python)

### Mac-Specific Setup
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3.9+
brew install python@3.11

# Install PostgreSQL
brew install postgresql
brew services start postgresql

# Install Docker Desktop
brew install --cask docker
```

---

## Project Setup

### 1. Clone Repository
```bash
cd /Users/tatejones/Coding/Projects/DrinkShelf
git clone https://github.com/tatejones2/DrinkShelf.git .
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip
```

### 3. Create .env File
Create a `.env` file in the project root:

```env
# Environment
ENVIRONMENT=development

# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/drinkshelf_dev

# OpenAI
OPENAI_API_KEY=your_openai_api_key_here

# Security
SECRET_KEY=your-secret-key-here-use-a-strong-random-string
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# API
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8080"]

# Logging
LOG_LEVEL=INFO
```

### 4. Set Up Database

#### Option A: Using PostgreSQL Directly
```bash
# Start PostgreSQL (Mac)
brew services start postgresql

# Create database
createdb drinkshelf_dev

# Create database user (optional)
psql -U postgres -c "CREATE USER drinkshelf_user WITH PASSWORD 'secure_password';"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE drinkshelf_dev TO drinkshelf_user;"
```

#### Option B: Using Docker (Recommended)
```bash
# Create docker-compose.yml in project root
# See section below for docker-compose.yml content

# Start services
docker-compose up -d

# Verify PostgreSQL is running
docker-compose ps
```

### 5. Install Dependencies
```bash
# Install required packages
pip install -r requirements.txt

# Or using poetry
poetry install
```

### 6. Run Database Migrations
```bash
# Initialize Alembic (first time only)
alembic init -t async migrations

# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head

# Verify migration
psql drinkshelf_dev -c "\dt"  # List all tables
```

### 7. Start Development Server
```bash
# Navigate to project directory
cd app

# Start FastAPI development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`
- API documentation: `http://localhost:8000/docs` (Swagger UI)
- Alternative documentation: `http://localhost:8000/redoc` (ReDoc)

---

## Docker Setup (Alternative)

### docker-compose.yml
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: drinkshelf_postgres
    environment:
      POSTGRES_USER: drinkshelf_user
      POSTGRES_PASSWORD: secure_password
      POSTGRES_DB: drinkshelf_dev
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U drinkshelf_user"]
      interval: 10s
      timeout: 5s
      retries: 5

  api:
    build: .
    container_name: drinkshelf_api
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://drinkshelf_user:secure_password@postgres:5432/drinkshelf_dev
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - SECRET_KEY=${SECRET_KEY}
      - ENVIRONMENT=development
    depends_on:
      postgres:
        condition: service_healthy
    volumes:
      - .:/app
    working_dir: /app

volumes:
  postgres_data:
```

### Running with Docker
```bash
# Build and start services
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down

# Stop and remove volumes (clean slate)
docker-compose down -v
```

---

## requirements.txt

```
# Web Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6

# Database
sqlalchemy==2.0.23
alembic==1.12.1
psycopg2-binary==2.9.9

# Authentication & Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0
PyJWT==2.8.1

# Data Validation
pydantic==2.5.0
pydantic-settings==2.1.0
email-validator==2.1.0

# AI Integration
openai==1.3.9

# Utilities
requests==2.31.0
httpx==0.25.2

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
httpx==0.25.2

# Code Quality
black==23.12.0
flake8==6.1.0
pylint==3.0.3
mypy==1.7.1

# Logging
python-json-logger==2.0.7

# CORS
fastapi-cors==0.0.6

# Environment management
python-dotenv==1.0.0
```

---

## Running Tests

### Setup Test Database
```bash
# Create test database
createdb drinkshelf_test

# Or with Docker
docker-compose exec postgres createdb -U drinkshelf_user drinkshelf_test
```

### Run Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v

# Run specific test function
pytest tests/test_auth.py::test_user_registration

# Run tests matching a pattern
pytest -k "test_bottle"
```

---

## Project Structure Overview

### app/main.py
Entry point for the FastAPI application. Sets up the app instance, includes routes, middleware, and startup/shutdown events.

### app/config.py
Centralized configuration management using Pydantic settings. Loads environment variables.

### app/models/
SQLAlchemy ORM models representing database tables:
- `user.py` - User model
- `bottle.py` - Bottle model
- `collection.py` - Collection model
- `tasting_note.py` - TastingNote model

### app/schemas/
Pydantic schemas for request/response validation:
- Maps to models but used for API contracts
- Includes validation rules and type hints

### app/crud/
CRUD (Create, Read, Update, Delete) operations:
- Database-level operations
- Reusable across different routes

### app/api/routes/
API endpoint definitions organized by resource:
- `auth.py` - Authentication endpoints
- `bottles.py` - Bottle CRUD
- `collections.py` - Collection management
- `search.py` - Search functionality
- `ai.py` - AI integration endpoints

### app/services/
Business logic layer:
- `ai_service.py` - OpenAI API interactions
- `bottle_classifier.py` - Spirit type classification
- `search_service.py` - Search logic

### app/database/
Database configuration:
- Connection pooling
- Session management
- Base class for models

### migrations/
Alembic migration files for database schema changes

### tests/
Test files mirroring app structure

---

## Common Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Start development server
uvicorn app.main:app --reload

# Create new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# Check code style
black --check app/
flake8 app/

# Format code
black app/

# Run type checking
mypy app/

# View database schema
psql drinkshelf_dev -c "\d"

# Open PostgreSQL CLI
psql drinkshelf_dev
```

---

## Troubleshooting

### PostgreSQL Connection Issues
```bash
# Check if PostgreSQL is running
brew services list | grep postgresql

# Restart PostgreSQL
brew services restart postgresql

# Check PostgreSQL logs
tail -f /usr/local/var/log/postgres.log
```

### Port Already in Use
```bash
# Find what's using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>
```

### Database Migration Issues
```bash
# Downgrade to previous state
alembic downgrade -1

# Reset to empty database
alembic downgrade base

# View migration history
alembic history
```

### OpenAI API Issues
- Verify API key in .env file
- Check API key has proper permissions
- Monitor API usage in OpenAI dashboard
- Implement retry logic for failed requests

---

## Development Workflow

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/description
   ```

2. **Make Changes**
   - Add models, schemas, routes as needed
   - Write tests for new functionality

3. **Run Tests**
   ```bash
   pytest
   ```

4. **Format Code**
   ```bash
   black app/
   flake8 app/
   ```

5. **Commit Changes**
   ```bash
   git add .
   git commit -m "Descriptive commit message"
   ```

6. **Push and Create Pull Request**
   ```bash
   git push origin feature/description
   ```

---

## Environment-Specific Configuration

### Development
- Debug mode: ON
- CORS: Allow localhost
- Database: Local PostgreSQL
- Logging: Verbose

### Production
- Debug mode: OFF
- CORS: Specific domains only
- Database: Remote PostgreSQL
- Logging: Standard
- OpenAI: Production keys
- HTTPS: Enforced

---

## Next Steps

1. Complete project setup following the above steps
2. Run tests to verify everything works
3. Access Swagger UI at http://localhost:8000/docs
4. Begin implementing Phase 1 features
5. Create database migrations as models are updated
6. Write tests alongside new features
