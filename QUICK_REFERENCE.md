# DrinkShelf - Quick Reference & Developer Guide

## Quick Start

```bash
# Clone and setup
cd /Users/tatejones/Coding/Projects/DrinkShelf
git clone https://github.com/tatejones2/DrinkShelf.git .
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your values

# Database setup
createdb drinkshelf_dev
alembic upgrade head

# Run development server
uvicorn app.main:app --reload

# Open browser to http://localhost:8000/docs
```

---

## File Organization Quick Reference

```
DrinkShelf/
├── app/
│   ├── models/          # SQLAlchemy models (database schema)
│   ├── schemas/         # Pydantic schemas (API request/response)
│   ├── crud/            # Database operations
│   ├── api/routes/      # API endpoints
│   ├── services/        # Business logic (AI, search, etc.)
│   ├── utils/           # Helper functions
│   ├── database/        # DB config and sessions
│   └── main.py          # FastAPI app initialization
├── migrations/          # Alembic database migrations
├── tests/               # Test files
├── PROJECT_OVERVIEW.md
├── TECHNICAL_SPECIFICATIONS.md
├── DEVELOPMENT_SETUP.md
├── DESIGN_GUIDELINES.md
├── IMPLEMENTATION_ROADMAP.md
└── requirements.txt
```

---

## Common Development Tasks

### Add a New API Endpoint

1. **Create model** (if needed) in `app/models/`
2. **Create schema** in `app/schemas/` for request/response validation
3. **Create CRUD operations** in `app/crud/`
4. **Create route** in `app/api/routes/`
5. **Include route** in `app/api/router.py`
6. **Write tests** in `tests/`

Example:
```python
# 1. Model: app/models/my_model.py
class MyModel(Base):
    __tablename__ = "my_models"
    id: UUID = Column(UUID, primary_key=True, default=uuid4)
    # ... fields

# 2. Schema: app/schemas/my_model.py
class MyModelCreate(BaseModel):
    # ... fields

# 3. CRUD: app/crud/my_model.py
async def create_item(db: Session, obj_in: MyModelCreate) -> MyModel:
    # ... logic

# 4. Route: app/api/routes/my_model.py
@router.post("/my-models")
async def create_my_model(obj: MyModelCreate, db: Session = Depends(get_db)):
    return await crud.create_item(db, obj)

# 5. Include in app/api/router.py
from .routes import my_model
app.include_router(my_model.router, prefix="/api", tags=["my-model"])

# 6. Test: tests/test_my_model.py
def test_create_my_model(client):
    # ... test logic
```

### Add Database Fields

1. Edit model in `app/models/`
2. Create migration: `alembic revision --autogenerate -m "Add field X to model Y"`
3. Review migration in `migrations/versions/`
4. Run migration: `alembic upgrade head`
5. Update schemas in `app/schemas/`
6. Update routes if needed

### Run Tests

```bash
# All tests
pytest

# Specific file
pytest tests/test_bottles.py

# Specific function
pytest tests/test_bottles.py::test_create_bottle

# With coverage
pytest --cov=app --cov-report=html

# Watch mode (requires pytest-watch)
ptw
```

### Database Debugging

```bash
# Connect to database
psql drinkshelf_dev

# List tables
\dt

# Describe table
\d bottles

# View rows
SELECT * FROM bottles;

# View schema
\d+ bottles

# Quit
\q
```

### Code Quality Checks

```bash
# Format code
black app/

# Lint code
flake8 app/

# Type check
mypy app/

# All at once
black app/ && flake8 app/ && mypy app/
```

---

## API Response Format Standards

### Successful Response
```json
{
  "id": "uuid-string",
  "field1": "value1",
  "field2": "value2",
  "created_at": "2025-01-01T12:00:00Z",
  "updated_at": "2025-01-01T12:00:00Z"
}
```

### List Response
```json
{
  "items": [
    { "id": "uuid", "field": "value" },
    { "id": "uuid", "field": "value" }
  ],
  "total": 100,
  "page": 1,
  "limit": 20,
  "pages": 5
}
```

### Error Response
```json
{
  "detail": "User not found",
  "code": "USER_NOT_FOUND",
  "timestamp": "2025-01-01T12:00:00Z"
}
```

---

## Environment Variables Reference

```env
# Application
ENVIRONMENT=development  # development|staging|production
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/drinkshelf_dev

# OpenAI
OPENAI_API_KEY=sk-...

# API Server
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=["http://localhost:3000"]

# Logging
LOG_LEVEL=INFO

# Optional
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20
REDIS_URL=redis://localhost:6379
```

---

## Dependency Versions

Key dependencies and versions:
- `fastapi==0.104.1` - Web framework
- `sqlalchemy==2.0.23` - ORM
- `psycopg2-binary==2.9.9` - PostgreSQL driver
- `alembic==1.12.1` - Migrations
- `pydantic==2.5.0` - Data validation
- `openai==1.3.9` - OpenAI API
- `pytest==7.4.3` - Testing
- `python-jose==3.3.0` - JWT handling

Check `requirements.txt` for complete list.

---

## Git Workflow

```bash
# Create feature branch
git checkout -b feature/bottle-search

# Make changes and commit
git add .
git commit -m "Add bottle search functionality"

# Push branch
git push origin feature/bottle-search

# Create Pull Request on GitHub
# After review and approval:

# Merge to main
git checkout main
git pull origin main
git merge feature/bottle-search
git push origin main

# Delete feature branch
git branch -d feature/bottle-search
git push origin --delete feature/bottle-search
```

### Commit Message Format
```
Type: Brief description

- Detailed bullet point 1
- Detailed bullet point 2

Fixes: #123 (if applicable)
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

---

## Debugging Tips

### Print Debugging
```python
import logging
logger = logging.getLogger(__name__)

logger.info(f"Variable value: {variable}")
logger.error(f"Error occurred: {error}")
```

### Database Debugging
```python
# In SQLAlchemy query
from sqlalchemy import event
from sqlalchemy.engine import Engine

@event.listens_for(Engine, "before_cursor_execute")
def receive_before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    print("STATEMENT:", statement)
    print("PARAMETERS:", parameters)
```

### API Testing
```bash
# Using curl
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"pass123","username":"testuser"}'

# Using httpie
http POST localhost:8000/auth/register email=test@example.com password=pass123 username=testuser

# Using Python requests
import requests
response = requests.post('http://localhost:8000/auth/register', 
    json={'email': 'test@example.com', 'password': 'pass123', 'username': 'testuser'})
```

---

## Performance Profiling

### Database Queries
```python
# Add to settings for query logging
SQLALCHEMY_ECHO = True  # In development only
```

### API Response Time
```bash
# Using httpie
http --timer localhost:8000/api/bottles

# Using curl with timing
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/api/bottles
```

### Memory Usage
```bash
# Using memory_profiler
pip install memory-profiler

# In code:
from memory_profiler import profile

@profile
def my_function():
    # code here
    pass
```

---

## Common Issues & Solutions

### Issue: "Table already exists"
```bash
# Downgrade to previous state
alembic downgrade -1

# View migration history
alembic history
```

### Issue: Port 8000 already in use
```bash
# Find process using port
lsof -i :8000

# Kill process
kill -9 <PID>
```

### Issue: PostgreSQL connection refused
```bash
# Check if PostgreSQL is running
brew services list | grep postgresql

# Start PostgreSQL
brew services start postgresql

# Check connection
psql -U postgres
```

### Issue: Permission denied on venv
```bash
# Ensure venv is activated
source venv/bin/activate

# Check Python path
which python  # Should show path with venv
```

### Issue: Module not found
```bash
# Ensure venv is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

---

## Monitoring & Logging

### Accessing Logs
```bash
# FastAPI logs (in terminal where server is running)
# Appears in real-time

# Database logs
tail -f /usr/local/var/log/postgres.log

# Application logs (if file-based)
tail -f logs/app.log
```

### Health Check Endpoint
```bash
curl http://localhost:8000/health

# Response:
# {"status": "ok", "timestamp": "2025-01-01T12:00:00Z"}
```

---

## Documentation References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)

---

## Support & Escalation

### Levels of Support
1. **Self-service**: Check documentation and existing code
2. **Peer review**: Ask team members in code review
3. **External resources**: Stack Overflow, GitHub issues, official docs
4. **Escalation**: Document issue, create GitHub issue, contact maintainer

### Creating an Issue
```markdown
# Title: Clear description of issue

## Description
Detailed explanation of what's happening

## Steps to Reproduce
1. Do this
2. Then this
3. Result: something breaks

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: macOS 12.6
- Python: 3.11
- FastAPI: 0.104.1
```

---

## Best Practices

### Code Organization
- One model per file
- One CRUD module per model
- Schemas grouped by domain
- Routes grouped by resource

### Testing
- Test every endpoint
- Test error cases
- Use fixtures for common data
- Mock external services (OpenAI)

### Performance
- Use database indexes
- Paginate large result sets
- Cache expensive operations
- Optimize N+1 queries

### Security
- Validate all inputs
- Use parameterized queries (SQLAlchemy handles this)
- Never log sensitive data
- Use HTTPS in production
- Rotate API keys regularly

### Documentation
- Docstrings on all functions
- Type hints on all parameters
- Comments for complex logic
- Update README for new features

---

## Phase 1 Checklist

Before moving to Phase 2, ensure:

- [ ] Project structure complete
- [ ] Docker working correctly
- [ ] PostgreSQL connected and migrations running
- [ ] Authentication system complete and tested
- [ ] User management endpoints working
- [ ] Tests for all Phase 1 features (>80% coverage)
- [ ] Code style checks passing (Black, Flake8)
- [ ] Type checking passing (MyPy)
- [ ] API documentation (Swagger) accessible
- [ ] README.md complete
- [ ] Git repository setup with branches
- [ ] Team trained on development setup

---

## Useful Aliases (Optional)

Add to `~/.zshrc` or `~/.bashrc`:

```bash
# DrinkShelf shortcuts
alias ds='cd /Users/tatejones/Coding/Projects/DrinkShelf'
alias dsenv='source venv/bin/activate'
alias dsrun='uvicorn app.main:app --reload'
alias dstest='pytest --cov=app'
alias dsformat='black app/ && flake8 app/'
```

Then use: `ds && dsenv && dsrun`
