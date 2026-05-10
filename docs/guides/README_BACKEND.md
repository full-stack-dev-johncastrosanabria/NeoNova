# NeoNova Backend

FastAPI-based backend for the NeoNova AI Assistant with Clean Architecture and Domain-Driven Design.

## 🏗️ Architecture

**Clean Architecture Layers:**
- **API Layer** (`src/api/`): HTTP routes, request/response schemas, authentication
- **Application Layer** (`src/application/`): Use cases, services, DTOs, interfaces
- **Domain Layer** (`src/domain/`): Entities, value objects, business rules
- **Infrastructure Layer** (`src/infrastructure/`): Database, external services, repositories

**Key Features:**
- JWT-based authentication with bcrypt password hashing
- PostgreSQL database with SQLAlchemy ORM
- Alembic database migrations
- OpenAI integration for AI responses
- Memory system for user preferences and context
- Comprehensive test suite with property-based testing
- Clean separation of concerns

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- PostgreSQL 14+
- OpenAI API key

### Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .[dev]

# Setup environment
cp .env.example .env
# Edit .env with your configuration

# Setup database
createdb neonova_dev
alembic upgrade head

# Run development server
uvicorn src.main:app --reload
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test types
pytest tests/unit/              # Unit tests
pytest tests/integration/       # Integration tests
pytest tests/properties/        # Property-based tests

# Run tests with verbose output
pytest -v

# Run specific test file
pytest tests/unit/test_user_entity.py
```

## 📁 Project Structure

```
backend/
├── src/
│   ├── api/                    # API Layer
│   │   ├── routes/            # HTTP route handlers
│   │   ├── schemas/           # Pydantic request/response models
│   │   ├── auth.py            # Authentication utilities
│   │   └── dependencies.py    # FastAPI dependencies
│   ├── application/           # Application Layer
│   │   ├── dtos/             # Data Transfer Objects
│   │   ├── interfaces/       # Abstract interfaces
│   │   ├── services/         # Application services
│   │   ├── use_cases/        # Business use cases
│   │   └── config.py         # Configuration
│   ├── domain/               # Domain Layer
│   │   ├── entities/         # Domain entities
│   │   ├── value_objects/    # Value objects
│   │   ├── enums.py          # Domain enumerations
│   │   └── exceptions.py     # Domain exceptions
│   ├── infrastructure/       # Infrastructure Layer
│   │   ├── database/         # Database configuration
│   │   ├── repositories/     # Data access implementations
│   │   ├── external/         # External service integrations
│   │   └── llm/             # LLM provider implementations
│   └── main.py              # FastAPI application entry point
├── tests/
│   ├── unit/                # Unit tests
│   ├── integration/         # Integration tests
│   ├── properties/          # Property-based tests
│   └── conftest.py          # Test configuration
├── alembic/                 # Database migrations
├── pyproject.toml          # Python project configuration
└── .env.example            # Environment template
```

## 🔧 Development

### Code Style
- **Formatter**: Black
- **Import Sorting**: isort
- **Type Checking**: mypy
- **Linting**: pylint (optional)

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Type checking
mypy src/

# Run all quality checks
black --check src/ tests/
isort --check-only src/ tests/
mypy src/
```

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Add new table"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# Show migration history
alembic history

# Show current revision
alembic current
```

### Environment Configuration

Create `.env` file with:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost/neonova_dev

# Authentication
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI
OPENAI_API_KEY=your-openai-api-key

# Application
ENVIRONMENT=development
DEBUG=true
```

## 🌐 API Documentation

When running the server, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### Key Endpoints

**Authentication:**
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `POST /auth/refresh` - Refresh access token

**Conversations:**
- `GET /conversations/` - List user conversations
- `POST /conversations/` - Create new conversation
- `GET /conversations/{id}` - Get conversation details
- `DELETE /conversations/{id}` - Delete conversation

**Messages:**
- `GET /conversations/{id}/messages` - Get conversation messages
- `POST /conversations/{id}/messages` - Send message to AI

**Memory:**
- `GET /memory/` - Get user memories
- `POST /memory/` - Create memory
- `PUT /memory/{id}` - Update memory
- `DELETE /memory/{id}` - Delete memory

**Feedback:**
- `POST /messages/{id}/feedback` - Provide message feedback

## 🧪 Testing Strategy

### Unit Tests
- Test individual components in isolation
- Mock external dependencies
- Focus on business logic and domain rules

### Integration Tests
- Test component interactions
- Use test database
- Test API endpoints end-to-end

### Property-Based Tests
- Use Hypothesis for property-based testing
- Test domain entity invariants
- Validate business rules under various conditions

### Test Configuration
```python
# conftest.py
@pytest.fixture
def test_db():
    # Setup test database
    pass

@pytest.fixture
def client():
    # FastAPI test client
    pass

@pytest.fixture
def authenticated_user():
    # User with valid JWT token
    pass
```

## 🚀 Deployment

### Production Setup
```bash
# Install production dependencies
pip install -e .

# Set production environment variables
export ENVIRONMENT=production
export DEBUG=false

# Run with gunicorn
gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Docker Deployment
```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY . .

RUN pip install -e .

CMD ["gunicorn", "src.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

## 🔍 Monitoring & Logging

### Health Checks
- `GET /health` - Application health status
- `GET /health/db` - Database connectivity

### Logging
```python
import logging

logger = logging.getLogger(__name__)
logger.info("Application started")
```

## 🛠️ Troubleshooting

### Common Issues

**Import Errors:**
```bash
# Ensure you're in the backend directory
cd backend

# Activate virtual environment
source venv/bin/activate

# Install in development mode
pip install -e .[dev]
```

**Database Connection:**
```bash
# Check PostgreSQL is running
pg_ctl status

# Test connection
psql -d neonova_dev -c "SELECT 1;"

# Check DATABASE_URL in .env
```

**Migration Issues:**
```bash
# Reset migrations (development only)
alembic downgrade base
alembic upgrade head

# Check migration files
ls alembic/versions/
```

**Test Failures:**
```bash
# Run tests with verbose output
pytest -v -s

# Run specific failing test
pytest tests/unit/test_specific.py::test_function -v

# Check test database
pytest --setup-show
```

### Performance Optimization

**Database Queries:**
- Use SQLAlchemy query optimization
- Add database indexes for frequent queries
- Use connection pooling

**API Performance:**
- Implement response caching
- Use async/await for I/O operations
- Add request/response compression

**Memory Usage:**
- Monitor memory consumption
- Implement pagination for large datasets
- Use lazy loading for relationships