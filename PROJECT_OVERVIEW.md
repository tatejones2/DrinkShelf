# DrinkShelf - Development Documentation

## 1. Project Overview

### Vision
DrinkShelf is a digital platform for spirit collectors to catalog, organize, and share their collections. Users maintain a personal digital shelf where they can track bottles, details, tasting notes, and preferences.

### Target Audience
- Whiskey and spirit enthusiasts
- Collectors and connoisseurs
- Casual drinkers who want to track their collections

### Key Features
- **Digital Shelf Management**: Add, edit, delete bottles from personal collection
- **AI-Powered Bottle Research**: OpenAI integration to populate bottle details automatically
- **Bottle Classification**: Automatic categorization (Whiskey, Vodka, Tequila, Beer, Other)
- **Bottle Details**: Proof, age statement, distillery, production details, price, tasting notes
- **Collection Insights**: Statistics and analytics about the collection
- **Search & Filter**: Find bottles by type, distillery, proof, price range, etc.

### Theme & Design Aesthetic
**Modern Heritage / Refined Speakeasy**
- Elegant, dark color palette with warm accents (gold, copper, amber)
- Sophisticated typography with vintage influences
- Clean, minimalist layout with high-quality imagery
- Professional yet inviting atmosphere

---

## 2. Technical Stack

### Backend
- **Framework**: FastAPI (Python 3.9+)
- **Database**: PostgreSQL 13+
- **ORM**: SQLAlchemy
- **API Documentation**: OpenAPI/Swagger (built-in with FastAPI)

### Frontend (To be determined)
- React/Vue.js with TypeScript recommended
- Tailwind CSS for styling
- Mobile-responsive design

### External Services
- **OpenAI API**: GPT-4 for bottle research and details extraction
- **Authentication**: JWT tokens

### Development Tools
- Docker for containerization
- Alembic for database migrations
- Pytest for testing
- Black/Flake8 for code formatting

---

## 3. Architecture Overview

### High-Level Architecture
```
┌─────────────────┐
│   Frontend      │
│  (React/Vue)    │
└────────┬────────┘
         │
         │ HTTP/REST
         │
┌────────▼────────────────┐
│    FastAPI Backend      │
│  ┌────────────────────┐ │
│  │  API Routes        │ │
│  │  - Users           │ │
│  │  - Bottles         │ │
│  │  - Collections     │ │
│  │  - Search          │ │
│  └────────────────────┘ │
│  ┌────────────────────┐ │
│  │  Business Logic    │ │
│  │  - AI Integration  │ │
│  │  - Validation      │ │
│  └────────────────────┘ │
└────────┬────────────────┘
         │
    ┌────▼─────┐
    │PostgreSQL│
    │Database  │
    └──────────┘
         ▲
         │
    ┌────┴──────────┐
    │  OpenAI API   │
    └───────────────┘
```

---

## 4. Database Schema

### Core Tables

#### Users
```sql
- id (UUID, PK)
- username (VARCHAR, UNIQUE)
- email (VARCHAR, UNIQUE)
- password_hash (VARCHAR)
- display_name (VARCHAR)
- bio (TEXT, optional)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
```

#### Bottles
```sql
- id (UUID, PK)
- user_id (UUID, FK → Users)
- name (VARCHAR)
- spirit_type (ENUM: whiskey, vodka, tequila, beer, other)
- distillery (VARCHAR)
- proof (FLOAT, optional)
- age_statement (VARCHAR, optional)
- region (VARCHAR, optional)
- country (VARCHAR, optional)
- release_year (INT, optional)
- batch_number (VARCHAR, optional)
- price_paid (DECIMAL, optional)
- price_current (DECIMAL, optional)
- acquisition_date (DATE, optional)
- notes (TEXT)
- rating (INT, 1-5, optional)
- image_url (VARCHAR, optional)
- ai_details (JSONB) # Stores OpenAI-generated details
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
- deleted_at (TIMESTAMP, soft delete)
```

#### Collections
```sql
- id (UUID, PK)
- user_id (UUID, FK → Users)
- name (VARCHAR)
- description (TEXT, optional)
- is_public (BOOLEAN)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
```

#### CollectionBottles
```sql
- id (UUID, PK)
- collection_id (UUID, FK → Collections)
- bottle_id (UUID, FK → Bottles)
- position (INT)
- added_at (TIMESTAMP)
```

#### TastingNotes
```sql
- id (UUID, PK)
- bottle_id (UUID, FK → Bottles)
- user_id (UUID, FK → Users)
- nose (TEXT)
- palate (TEXT)
- finish (TEXT)
- overall_notes (TEXT)
- rating (INT, 1-5)
- tasted_date (DATE)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
```

---

## 5. API Endpoints

### Authentication
- `POST /auth/register` - Create new user account
- `POST /auth/login` - Authenticate and receive JWT token
- `POST /auth/refresh` - Refresh JWT token
- `POST /auth/logout` - Invalidate token

### Users
- `GET /users/{user_id}` - Get user profile
- `PUT /users/{user_id}` - Update user profile
- `GET /users/{user_id}/statistics` - Get collection statistics

### Bottles
- `POST /bottles` - Add new bottle (with AI research)
- `GET /bottles/{bottle_id}` - Get bottle details
- `PUT /bottles/{bottle_id}` - Update bottle
- `DELETE /bottles/{bottle_id}` - Delete bottle (soft delete)
- `GET /bottles` - List user's bottles (with pagination/filtering)

### Collections
- `POST /collections` - Create new collection
- `GET /collections/{collection_id}` - Get collection details
- `PUT /collections/{collection_id}` - Update collection
- `DELETE /collections/{collection_id}` - Delete collection
- `GET /collections/{collection_id}/bottles` - Get bottles in collection
- `POST /collections/{collection_id}/bottles/{bottle_id}` - Add bottle to collection
- `DELETE /collections/{collection_id}/bottles/{bottle_id}` - Remove bottle from collection

### Search & Discovery
- `GET /search?query=...&type=...&proof_min=...&proof_max=...` - Search bottles
- `GET /trending` - Get trending bottles across platform

### AI Research
- `POST /ai/research-bottle` - Research bottle details using OpenAI
- `GET /ai/research-status/{request_id}` - Check research status

### Tasting Notes
- `POST /bottles/{bottle_id}/tasting-notes` - Add tasting notes
- `GET /bottles/{bottle_id}/tasting-notes` - Get tasting notes
- `PUT /tasting-notes/{note_id}` - Update tasting notes
- `DELETE /tasting-notes/{note_id}` - Delete tasting notes

---

## 6. AI Integration Strategy

### OpenAI API Usage
When a user adds a new bottle, the system will:

1. **Initial Input**: User provides bottle name (e.g., "1792 Small Batch Bourbon")
2. **AI Query**: Send to OpenAI GPT-4 with structured prompt
3. **Data Extraction**: Parse response to extract and validate information
4. **Storage**: Store both raw AI response and parsed details

### Prompt Structure
```
You are an expert in spirits and beverages. Provide detailed information about the following bottle:

Bottle: {bottle_name}

Return the information in JSON format with these fields:
{
  "spirit_type": "whiskey|vodka|tequila|beer|other",
  "distillery": "...",
  "proof": number,
  "age_statement": "...",
  "region": "...",
  "country": "...",
  "release_year": number or null,
  "notes": "...",
  "key_characteristics": ["...", "..."],
  "price_range": "...",
  "availability": "..."
}

Ensure accuracy. If uncertain about a field, use null.
```

### Error Handling
- If OpenAI API fails, allow manual entry
- Cache frequently researched bottles
- Implement rate limiting and request queuing

---

## 7. Frontend Requirements

### Pages/Views
1. **Landing Page** - Introduction and value proposition
2. **Authentication** - Login/Register pages
3. **Dashboard** - User's main collection view
4. **Add Bottle** - Form with AI-powered research
5. **Bottle Detail** - Full bottle information and tasting notes
6. **Collections** - Organize bottles into custom collections
7. **Search** - Discover and filter bottles
8. **Profile** - User preferences and settings
9. **Analytics** - Collection statistics and insights

### UI Components
- Bottle card component with image and key details
- Shelf visualization (grid/list view toggle)
- Search/filter bar
- Modal for adding/editing bottles
- Rating stars
- Tasting note input form
- Authentication forms

---

## 8. Development Phases

### Phase 1: Foundation (Weeks 1-2)
- [ ] Project setup and environment configuration
- [ ] Database schema and migrations
- [ ] User authentication system
- [ ] Basic user profile endpoints
- [ ] PostgreSQL setup and connection

### Phase 2: Core Features (Weeks 3-4)
- [ ] Bottle model and CRUD operations
- [ ] OpenAI API integration for bottle research
- [ ] Bottle classification logic
- [ ] Search and filtering logic
- [ ] Collection management

### Phase 3: Enhancement (Week 5)
- [ ] Tasting notes feature
- [ ] User statistics and analytics
- [ ] Image upload and management
- [ ] Advanced filtering options

### Phase 4: Frontend (Weeks 6+)
- [ ] React/Vue application setup
- [ ] Component library creation
- [ ] Integration with backend APIs
- [ ] User interface implementation
- [ ] Theming and styling

### Phase 5: Polish & Launch (Ongoing)
- [ ] Testing and QA
- [ ] Performance optimization
- [ ] Security audit
- [ ] Deployment setup

---

## 9. Security Considerations

- JWT authentication with expiration
- Password hashing (bcrypt)
- CORS configuration
- Input validation and sanitization
- SQL injection prevention (SQLAlchemy ORM)
- Rate limiting on API endpoints
- Environment variable management for secrets
- HTTPS enforcement
- API key rotation for OpenAI

---

## 10. Performance Considerations

- Database indexing on frequently queried fields
- Pagination for large datasets
- Caching layer for popular bottles
- Image optimization and CDN delivery
- Query optimization
- Connection pooling
- Async operations for AI research

---

## 11. Development Setup Instructions

### Prerequisites
- Python 3.9+
- PostgreSQL 13+
- pip/pipenv or poetry
- Docker (recommended)
- Git

### Initial Setup
1. Clone repository
2. Create virtual environment
3. Install dependencies
4. Set up environment variables
5. Create PostgreSQL database
6. Run migrations
7. Start development server

### Environment Variables
```
DATABASE_URL=postgresql://user:password@localhost:5432/drinkshelf
OPENAI_API_KEY=your_api_key
SECRET_KEY=your_jwt_secret
ENVIRONMENT=development
```

---

## 12. Testing Strategy

### Unit Tests
- Model validation
- API endpoint logic
- AI prompt generation and parsing

### Integration Tests
- Database operations
- API endpoints with database
- OpenAI API mocking

### End-to-End Tests
- Complete user workflows
- Full collection management

### Test Framework
- Pytest with fixtures
- Mock OpenAI responses
- Test database setup and teardown

---

## 13. Deployment

### Infrastructure
- Docker containerization
- PostgreSQL hosted database
- API deployment (Heroku, AWS, or similar)
- Frontend hosting (Vercel, Netlify, or similar)

### CI/CD
- GitHub Actions for automated testing
- Automated deployment on push to main
- Database migration automation

---

## 14. Success Metrics

- User can add a bottle with AI-researched details within 2 clicks
- AI accuracy for bottle details > 90%
- Page load time < 2 seconds
- API response time < 500ms
- 99.9% uptime
- User retention rate > 60%

---

## 15. Future Enhancements

- Social features (sharing collections, following users)
- Bottle marketplace integration
- AR bottle visualization
- Mobile app (React Native)
- Community ratings and reviews
- Price tracking and notifications
- Inventory management for bars/restaurants
- Export collection to PDF
- Advanced analytics dashboard
