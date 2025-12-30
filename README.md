# DrinkShelf Backend

A sophisticated digital platform for spirit collectors to catalog, organize, and share their collections.

## Features

- **Digital Shelf Management**: Add, edit, delete bottles from your personal collection
- **AI-Powered Bottle Research**: OpenAI integration to automatically populate bottle details
- **Bottle Classification**: Automatic categorization (Whiskey, Vodka, Tequila, Beer, Wine, etc.)
- **Collection Organization**: Organize bottles into custom collections
- **Tasting Notes**: Record and track tasting experiences
- **Search & Filter**: Find bottles by type, distillery, proof, price, country, and more
- **User Statistics**: View collection analytics and insights

## Tech Stack

- **Framework**: FastAPI (Python 3.9+)
- **Database**: PostgreSQL 13+
- **ORM**: SQLAlchemy
- **Authentication**: JWT tokens with bcrypt password hashing
- **AI**: OpenAI API integration
- **DevOps**: Docker & Docker Compose

## Quick Start

### Prerequisites

- Python 3.9+
- PostgreSQL 13+
- Docker & Docker Compose (optional)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/tatejones2/DrinkShelf.git
   cd DrinkShelf
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your values
   ```

5. **Create database**
   ```bash
   createdb drinkshelf_dev
   ```

6. **Run migrations**
   ```bash
   alembic upgrade head
   ```

7. **Start development server**
   ```bash
   uvicorn app.main:app --reload
   ```

Access the API at: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Docker Setup

Alternatively, use Docker:

```bash
# Build and start services
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

## Project Structure

```
app/
├── api/              # API routes and endpoints
├── crud/             # Database CRUD operations
├── database/         # Database configuration
├── models/           # SQLAlchemy models
├── schemas/          # Pydantic schemas
├── services/         # Business logic
├── utils/            # Helper functions
├── config.py         # Configuration management
└── main.py           # FastAPI app initialization

tests/                # Test files
migrations/           # Alembic migrations
docs/                 # Documentation
```

## Development

### Running Tests

```bash
pytest
pytest --cov=app --cov-report=html
```

### Code Quality

```bash
# Format code
black app/

# Lint code
flake8 app/

# Type check
mypy app/
```

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## API Documentation

See [docs/](docs/) for comprehensive documentation:

- [01_PROJECT_OVERVIEW.md](docs/01_PROJECT_OVERVIEW.md) - Project overview and architecture
- [02_TECHNICAL_SPECIFICATIONS.md](docs/02_TECHNICAL_SPECIFICATIONS.md) - Technical details
- [03_DEVELOPMENT_SETUP.md](docs/03_DEVELOPMENT_SETUP.md) - Setup guide
- [04_DESIGN_GUIDELINES.md](docs/04_DESIGN_GUIDELINES.md) - UI/UX guidelines
- [05_IMPLEMENTATION_ROADMAP.md](docs/05_IMPLEMENTATION_ROADMAP.md) - Development roadmap
- [06_QUICK_REFERENCE.md](docs/06_QUICK_REFERENCE.md) - Quick reference guide

## Environment Variables

Create a `.env` file based on `.env.example`:

```env
ENVIRONMENT=development
DATABASE_URL=postgresql://user:password@localhost:5432/drinkshelf_dev
OPENAI_API_KEY=your_api_key
SECRET_KEY=your-secret-key-min-32-chars
```

## Contributing

1. Create a feature branch: `git checkout -b feature/description`
2. Make changes and write tests
3. Format code: `black app/`
4. Lint code: `flake8 app/`
5. Commit: `git commit -m "feat: description"`
6. Push: `git push origin feature/description`
7. Create a Pull Request

## License

This project is proprietary and confidential.

## Support

For questions or issues, refer to the documentation or create a GitHub issue.

---

**Happy coding! 🍾**
