# NeoNova AI Assistant

NeoNova is a progressive AI assistant platform that combines conversational chat, persistent memory management, user feedback collection, and intelligent agent orchestration. Built with modern technologies and Clean Architecture principles, it provides a foundation for building personalized AI experiences.

## Overview

NeoNova AI Assistant is an MVP (Minimum Viable Product) designed to grow progressively. The platform integrates with leading LLM providers (OpenAI/Azure OpenAI) to deliver intelligent, context-aware conversations.

### Core Modules

- **Chat Module**: Conversational messaging with real-time AI responses
- **Memory Module**: Persistent storage of user preferences, facts, instructions, and corrections
- **Feedback Module**: User ratings and corrections that improve assistant responses
- **Agent Orchestration**: Intelligent prompt building with contextual memory and conversation history

### Tech Stack

- **Backend**: Python 3.12+, FastAPI, SQLAlchemy, PostgreSQL
- **Frontend**: React, TypeScript, Vite
- **Database**: PostgreSQL 14+
- **LLM Integration**: OpenAI API / Azure OpenAI
- **Containerization**: Docker & Docker Compose

## Architecture

NeoNova follows **Clean Architecture** principles with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────┐
│                    API Layer                             │
│         (FastAPI Routes, Auth, Schemas)                 │
├─────────────────────────────────────────────────────────┤
│              Application Layer                           │
│    (Use Cases, Services, Interfaces, DTOs)              │
├─────────────────────────────────────────────────────────┤
│                Domain Layer                              │
│         (Entities, Value Objects, Enums)                │
├─────────────────────────────────────────────────────────┤
│            Infrastructure Layer                          │
│  (Repositories, Models, LLM Providers, Database)        │
└─────────────────────────────────────────────────────────┘
```

For detailed architecture documentation, see [design.md](.kiro/specs/neonova-ai-assistant/design.md).

## Prerequisites

Before getting started, ensure you have the following installed:

- **Docker** 20.10+ and **Docker Compose** 2.0+
- **Node.js** 18+ (for local frontend development)
- **Python** 3.12+ (for local backend development)
- **PostgreSQL** 14+ (for local database development)
- **Git** for version control

### API Keys Required

- **OpenAI API Key** (if using OpenAI provider): Get from [platform.openai.com](https://platform.openai.com)
- **Azure OpenAI API Key** (if using Azure provider): Get from [Azure Portal](https://portal.azure.com)

## Quick Start (Docker)

The fastest way to get NeoNova running is with Docker Compose.

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/neonova.git
cd neonova
```

### 2. Configure Environment

Copy the Docker environment template:

```bash
cp .env.docker.example .env
```

Edit `.env` and add your LLM provider credentials:

```env
# LLM Provider Configuration
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-4o-mini
```

### 3. Start Services

```bash
docker-compose up
```

This will:
- Start PostgreSQL database (port 5432)
- Build and start the backend API (port 8000)
- Build and start the frontend (port 3000)

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### 5. Stop Services

```bash
docker-compose down
```

To also remove the database volume:

```bash
docker-compose down -v
```

## Local Development Setup

For development with hot-reload and debugging capabilities.

### Backend Setup

#### 1. Create Virtual Environment

```bash
cd backend
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 2. Install Dependencies

```bash
pip install -e ".[dev]"
```

#### 3. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your local database and LLM credentials:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/neonova
OPENAI_API_KEY=sk-your-openai-api-key-here
LLM_PROVIDER=openai
```

#### 4. Setup Database

Ensure PostgreSQL is running locally, then run migrations:

```bash
alembic upgrade head
```

#### 5. Start Backend Server

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at http://localhost:8000 with auto-reload on file changes.

### Frontend Setup

#### 1. Install Dependencies

```bash
cd frontend
npm install
```

#### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` to point to your backend:

```env
VITE_API_URL=http://localhost:8000
```

#### 3. Start Development Server

```bash
npm run dev
```

The frontend will be available at http://localhost:5173 with hot module replacement.

## Running Tests

### Unit Tests

Run all unit tests:

```bash
pytest backend/tests/
```

Run tests for a specific module:

```bash
pytest backend/tests/unit/
```

Run with coverage:

```bash
pytest backend/tests/ --cov=src --cov-report=html
```

### Property-Based Tests

Run property-based tests using Hypothesis:

```bash
pytest backend/tests/properties/
```

Property-based tests verify that properties hold across many randomly generated inputs.

### Integration Tests

Run integration tests (requires database):

```bash
pytest backend/tests/integration/
```

### Run All Tests

```bash
pytest backend/tests/ -v
```

## Environment Variables

### Backend Environment Variables

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+asyncpg://user:pass@localhost:5432/neonova` | Yes |
| `SECRET_KEY` | JWT signing secret key | `your-secret-key-change-in-production` | Yes |
| `ALGORITHM` | JWT algorithm | `HS256` | Yes |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT token expiration time | `30` | Yes |
| `LLM_PROVIDER` | LLM provider selection | `openai` or `azure` | Yes |
| `OPENAI_API_KEY` | OpenAI API key | `sk-...` | If using OpenAI |
| `OPENAI_MODEL` | OpenAI model name | `gpt-4o-mini` | If using OpenAI |
| `AZURE_OPENAI_API_KEY` | Azure OpenAI API key | `your-key` | If using Azure |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI endpoint | `https://resource.openai.azure.com/` | If using Azure |
| `AZURE_OPENAI_DEPLOYMENT_NAME` | Azure deployment name | `your-deployment` | If using Azure |
| `CORS_ALLOW_ORIGINS` | CORS allowed origins | `http://localhost:3000` | No |
| `DEBUG` | Debug mode | `false` | No |

### Frontend Environment Variables

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `VITE_API_URL` | Backend API URL | `http://localhost:8000` | Yes |

### Docker Environment Variables

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `POSTGRES_USER` | PostgreSQL username | `neonova` | Yes |
| `POSTGRES_PASSWORD` | PostgreSQL password | `neonova_dev_password` | Yes |
| `POSTGRES_DB` | PostgreSQL database name | `neonova` | Yes |

## API Endpoints

### Authentication

| Method | Path | Auth Required | Description |
|--------|------|---------------|-------------|
| POST | `/auth/register` | No | Register a new user account |
| POST | `/auth/login` | No | Authenticate user and receive JWT token |

### Conversations

| Method | Path | Auth Required | Description |
|--------|------|---------------|-------------|
| POST | `/conversations/` | Yes | Create a new conversation |
| GET | `/conversations/` | Yes | List all conversations for authenticated user |
| DELETE | `/conversations/{conversation_id}` | Yes | Delete a conversation |

### Messages

| Method | Path | Auth Required | Description |
|--------|------|---------------|-------------|
| POST | `/conversations/{conversation_id}/messages` | Yes | Send a message and receive AI response |
| GET | `/conversations/{conversation_id}/messages` | Yes | List all messages in a conversation |

### Memories

| Method | Path | Auth Required | Description |
|--------|------|---------------|-------------|
| GET | `/memories/` | Yes | List all active memories for user |
| POST | `/memories/` | Yes | Create a new memory |
| DELETE | `/memories/{memory_id}` | Yes | Deactivate a memory |

### Feedback

| Method | Path | Auth Required | Description |
|--------|------|---------------|-------------|
| POST | `/feedback/` | Yes | Submit feedback for a message |

### Health Check

| Method | Path | Auth Required | Description |
|--------|------|---------------|-------------|
| GET | `/health` | No | Check API health status |

## Project Structure

```
neonova/
├── backend/
│   ├── src/
│   │   ├── api/                 # API layer (routes, schemas, auth)
│   │   ├── application/         # Application layer (use cases, services)
│   │   ├── domain/              # Domain layer (entities, enums)
│   │   ├── infrastructure/      # Infrastructure layer (repos, models, db)
│   │   └── main.py              # FastAPI application entry point
│   ├── tests/
│   │   ├── unit/                # Unit tests
│   │   ├── integration/         # Integration tests
│   │   └── properties/          # Property-based tests
│   ├── alembic/                 # Database migrations
│   ├── pyproject.toml           # Python dependencies
│   └── Dockerfile               # Backend container image
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── pages/               # Page components
│   │   ├── services/            # API client services
│   │   ├── types/               # TypeScript types
│   │   └── App.tsx              # Main app component
│   ├── package.json             # Node dependencies
│   ├── vite.config.ts           # Vite configuration
│   └── Dockerfile               # Frontend container image
├── .env.docker.example          # Docker environment template
├── docker-compose.yml           # Docker Compose configuration
└── README.md                    # This file
```

## Management Scripts

NeoNova includes helpful scripts to manage development and testing workflows:

### Setup Development Environment

```bash
./scripts/setup-dev.sh
```

This script:
- Checks prerequisites (Python 3.12+, Node.js 18+, PostgreSQL 14+)
- Creates Python virtual environment
- Installs backend dependencies
- Installs frontend dependencies
- Sets up environment files (.env)
- Runs database migrations
- Verifies the setup with tests

Options:
- `--skip-db`: Skip database setup
- `--skip-verify`: Skip setup verification

### Manage Services

```bash
./scripts/manage-services.sh [COMMAND]
```

Commands:
- `start`: Start all services (backend + frontend)
- `stop`: Stop all services
- `restart`: Restart all services
- `status`: Show service status
- `logs [service]`: Show logs (all, backend, or frontend)
- `backend`: Start only backend service
- `frontend`: Start only frontend service

Examples:
```bash
./scripts/manage-services.sh start      # Start all services
./scripts/manage-services.sh status     # Check service status
./scripts/manage-services.sh logs       # Show all logs
./scripts/manage-services.sh logs backend  # Show backend logs
```

### Run All Tests

```bash
./scripts/test-all.sh [OPTIONS]
```

Options:
- `--backend-only`: Run only backend tests
- `--frontend-only`: Run only frontend tests
- `--with-lint`: Include linting checks

Examples:
```bash
./scripts/test-all.sh                   # Run all tests
./scripts/test-all.sh --backend-only    # Run backend tests only
./scripts/test-all.sh --with-lint       # Run tests with linting
```

## Development Workflow

### Making Changes

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and test locally

3. Run tests to ensure nothing breaks:
   ```bash
   ./scripts/test-all.sh
   ```

4. Commit and push:
   ```bash
   git add .
   git commit -m "feat: description of changes"
   git push origin feature/your-feature-name
   ```

5. Create a pull request for review

### Code Quality

- **Type Hints**: All Python code includes type hints
- **Validation**: Pydantic schemas validate all API inputs
- **Testing**: Aim for 80%+ code coverage
- **Clean Architecture**: Maintain clear layer separation

## Troubleshooting

### Database Connection Issues

If you get database connection errors:

1. Verify PostgreSQL is running:
   ```bash
   psql -U neonova -d neonova -c "SELECT 1"
   ```

2. Check DATABASE_URL in `.env` is correct

3. Run migrations:
   ```bash
   alembic upgrade head
   ```

### LLM Provider Errors

If you get LLM provider errors:

1. Verify API key is set correctly in `.env`
2. Check API key has appropriate permissions
3. Verify rate limits haven't been exceeded
4. Check network connectivity to provider

### Port Already in Use

If ports are already in use:

- Backend (8000): `lsof -i :8000` and kill the process
- Frontend (3000/5173): `lsof -i :3000` and kill the process
- Database (5432): `lsof -i :5432` and kill the process

### Docker Issues

If Docker containers won't start:

1. Check Docker daemon is running
2. Verify sufficient disk space
3. Clean up old containers: `docker-compose down -v`
4. Rebuild images: `docker-compose build --no-cache`

## Contributing

Contributions are welcome! Please:

1. Follow the existing code style and architecture
2. Write tests for new functionality
3. Update documentation as needed
4. Submit pull requests with clear descriptions

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Support

For issues, questions, or suggestions:

1. Check existing [GitHub Issues](https://github.com/yourusername/neonova/issues)
2. Create a new issue with detailed description
3. Include error messages and steps to reproduce

## Roadmap

Future enhancements planned for NeoNova:

- **RAG Module**: Retrieval-Augmented Generation for document-based context
- **Tools Module**: Safe execution of user-defined tasks
- **Advanced Memory**: Semantic search and automatic memory categorization
- **Analytics**: Usage analytics and performance monitoring
- **Multi-language Support**: Support for multiple languages
- **Mobile App**: Native mobile applications

---

**Last Updated**: 2024
**Version**: 0.1.0 (MVP)
