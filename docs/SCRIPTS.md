# NeoNova Scripts Guide

All management scripts are located in the `scripts/` directory and provide automated workflows for development, testing, and service management.

## Quick Reference

```bash
# Initial setup (one time)
./scripts/setup-dev.sh

# Start services
./scripts/manage-services.sh start

# Run tests
./scripts/test-all.sh

# Check status
./scripts/manage-services.sh status

# View logs
./scripts/manage-services.sh logs
```

---

## setup-dev.sh - Development Environment Setup

### Purpose

Automates the initial setup of the development environment, including:
- Prerequisite checking
- Virtual environment creation
- Dependency installation
- Environment file setup
- Database initialization
- Setup verification

### Usage

```bash
./scripts/setup-dev.sh [OPTIONS]
```

### Options

| Option | Description |
|--------|-------------|
| `--skip-db` | Skip database setup |
| `--skip-verify` | Skip verification tests |
| `--help` | Show help message |

### Examples

```bash
# Full setup with verification
./scripts/setup-dev.sh

# Skip database setup
./scripts/setup-dev.sh --skip-db

# Skip verification
./scripts/setup-dev.sh --skip-verify

# Show help
./scripts/setup-dev.sh --help
```

### What It Does

1. **Checks Prerequisites**
   - Python 3.12+
   - Node.js 18+
   - npm
   - PostgreSQL (optional)

2. **Backend Setup**
   - Creates Python virtual environment
   - Installs dependencies from `pyproject.toml`
   - Creates `.env` file from template
   - Installs development tools

3. **Frontend Setup**
   - Installs Node.js dependencies
   - Creates `.env` file from template

4. **Database Setup**
   - Creates PostgreSQL database
   - Runs Alembic migrations

5. **Verification**
   - Runs backend tests
   - Builds frontend
   - Reports any issues

### Output

```
[2024-05-08 12:00:00] Starting NeoNova development setup...
[2024-05-08 12:00:01] Checking prerequisites...
[2024-05-08 12:00:02] Found Python 3.12.0
[2024-05-08 12:00:02] Found Node.js v18.0.0
[2024-05-08 12:00:02] Found npm 9.0.0
[SUCCESS] Prerequisites check completed!
...
[SUCCESS] Development environment setup completed!
```

---

## manage-services.sh - Service Management

### Purpose

Manages backend and frontend services with:
- Service startup/shutdown
- Health checks
- Process monitoring
- Log streaming
- Status reporting

### Usage

```bash
./scripts/manage-services.sh [COMMAND]
```

### Commands

| Command | Description |
|---------|-------------|
| `start` | Start all services |
| `stop` | Stop all services |
| `restart` | Restart all services |
| `status` | Show service status |
| `logs [service]` | Show logs |
| `backend` | Start backend only |
| `frontend` | Start frontend only |
| `help` | Show help message |

### Examples

```bash
# Start all services
./scripts/manage-services.sh start

# Stop all services
./scripts/manage-services.sh stop

# Restart all services
./scripts/manage-services.sh restart

# Check service status
./scripts/manage-services.sh status

# View all logs
./scripts/manage-services.sh logs

# View backend logs
./scripts/manage-services.sh logs backend

# View frontend logs
./scripts/manage-services.sh logs frontend

# Start backend only
./scripts/manage-services.sh backend

# Start frontend only
./scripts/manage-services.sh frontend

# Show help
./scripts/manage-services.sh help
```

### Service Details

#### Backend Service
- **Port**: 8000
- **Framework**: FastAPI with Uvicorn
- **Reload**: Enabled (auto-restart on file changes)
- **Health Check**: `GET /health`
- **Logs**: `logs/backend.log`

#### Frontend Service
- **Port**: 5173
- **Framework**: Vite development server
- **Hot Reload**: Enabled (HMR)
- **Health Check**: HTTP GET to root
- **Logs**: `logs/frontend.log`

### Output

```
[2024-05-08 12:00:00] Starting all services...
[2024-05-08 12:00:01] Starting backend service...
[2024-05-08 12:00:02] Creating Python virtual environment...
[2024-05-08 12:00:05] Installing Python dependencies...
[2024-05-08 12:00:15] Launching FastAPI server...
[SUCCESS] Backend started with PID 12345
[2024-05-08 12:00:20] Checking backend health...
[SUCCESS] Backend is healthy (attempt 1/30)
[SUCCESS] Backend is running and healthy at http://localhost:8000
[2024-05-08 12:00:21] Starting frontend service...
[2024-05-08 12:00:22] Installing Node.js dependencies...
[2024-05-08 12:00:30] Launching Vite development server...
[SUCCESS] Frontend started with PID 12346
[SUCCESS] All services started successfully!
```

### Service URLs

When services are running:

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:5173 | React app |
| Backend API | http://localhost:8000 | FastAPI server |
| API Docs | http://localhost:8000/docs | Swagger UI |
| API ReDoc | http://localhost:8000/redoc | ReDoc documentation |

---

## test-all.sh - Test Runner

### Purpose

Runs all tests for backend and frontend with:
- Unit tests
- Integration tests
- Property-based tests
- Coverage reporting
- Optional linting

### Usage

```bash
./scripts/test-all.sh [OPTIONS]
```

### Options

| Option | Description |
|--------|-------------|
| `--backend-only` | Run only backend tests |
| `--frontend-only` | Run only frontend tests |
| `--with-lint` | Include linting checks |
| `--help` | Show help message |

### Examples

```bash
# Run all tests
./scripts/test-all.sh

# Backend tests only
./scripts/test-all.sh --backend-only

# Frontend tests only
./scripts/test-all.sh --frontend-only

# Include linting
./scripts/test-all.sh --with-lint

# Show help
./scripts/test-all.sh --help
```

### Backend Tests

```bash
# All backend tests
pytest backend/tests/

# Unit tests only
pytest backend/tests/unit/

# Integration tests only
pytest backend/tests/integration/

# Property-based tests only
pytest backend/tests/properties/

# With coverage
pytest backend/tests/ --cov=src --cov-report=html
```

### Frontend Tests

```bash
# All frontend tests
npm test

# Watch mode
npm test -- --watch

# Coverage
npm test -- --coverage
```

### Linting

```bash
# Python linting
black --check src/ tests/
isort --check-only src/ tests/
mypy src/

# JavaScript/TypeScript linting
npm run lint
```

### Output

```
[2024-05-08 12:00:00] Starting test suite...
[2024-05-08 12:00:01] Running backend tests...
[2024-05-08 12:00:02] Running Python tests with coverage...
======================== test session starts =========================
collected 150 items

tests/unit/test_auth.py ............................ [ 16%]
tests/unit/test_entities.py ........................ [ 32%]
tests/integration/test_auth_flow.py ............... [ 48%]
tests/properties/test_domain_properties.py ........ [ 64%]

======================== 150 passed in 12.34s =========================
[SUCCESS] Backend tests passed!
[2024-05-08 12:00:15] Running frontend tests...
[2024-05-08 12:00:20] Running JavaScript/TypeScript tests...
[SUCCESS] Frontend tests passed!
[SUCCESS] All tests completed successfully!
```

---

## Common Workflows

### First Time Setup

```bash
# 1. Run setup script
./scripts/setup-dev.sh

# 2. Edit environment files
# backend/.env - Add database and API credentials
# frontend/.env - Configure API URL

# 3. Start services
./scripts/manage-services.sh start

# 4. Access application
# Frontend: http://localhost:5173
# Backend: http://localhost:8000
```

### Daily Development

```bash
# Terminal 1: Start services
./scripts/manage-services.sh start

# Terminal 2: Run tests
./scripts/test-all.sh

# Terminal 3: View logs
./scripts/manage-services.sh logs
```

### Before Committing

```bash
# Run all tests with linting
./scripts/test-all.sh --with-lint

# Check service status
./scripts/manage-services.sh status

# View any errors
./scripts/manage-services.sh logs
```

### Troubleshooting

```bash
# Check service status
./scripts/manage-services.sh status

# View logs for debugging
./scripts/manage-services.sh logs backend

# Restart services
./scripts/manage-services.sh restart

# Full reset
./scripts/manage-services.sh stop
./scripts/setup-dev.sh --skip-verify
./scripts/manage-services.sh start
```

---

## Log Files

Logs are stored in the `logs/` directory:

```
logs/
├── backend.log    # Backend service logs
└── frontend.log   # Frontend service logs
```

### View Logs

```bash
# View all logs
./scripts/manage-services.sh logs

# View backend logs
./scripts/manage-services.sh logs backend

# View frontend logs
./scripts/manage-services.sh logs frontend

# Follow logs in real-time
tail -f logs/backend.log
tail -f logs/frontend.log
```

---

## Environment Files

### Backend (.env)

Located at `backend/.env`

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/neonova

# Authentication
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# LLM Provider
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-openai-api-key
OPENAI_MODEL=gpt-4o-mini

# CORS
CORS_ALLOW_ORIGINS=http://localhost:5173
```

### Frontend (.env)

Located at `frontend/.env`

```env
VITE_API_URL=http://localhost:8000
```

---

## Troubleshooting

### Port Already in Use

```bash
# Find process using port
lsof -i :8000  # Backend
lsof -i :5173  # Frontend

# Kill process
kill -9 <PID>

# Or restart services
./scripts/manage-services.sh restart
```

### Virtual Environment Issues

```bash
# Recreate virtual environment
rm -rf backend/venv
./scripts/setup-dev.sh --skip-verify
```

### Database Connection Failed

```bash
# Check PostgreSQL is running
psql -U neonova -d neonova -c "SELECT 1"

# Run migrations manually
cd backend
source venv/bin/activate
alembic upgrade head
```

### Tests Failing

```bash
# Run with verbose output
./scripts/test-all.sh --backend-only
cd backend && pytest -v

# Run specific test
pytest tests/unit/test_auth.py -v
```

### Services Won't Start

```bash
# Check logs
./scripts/manage-services.sh logs

# Verify prerequisites
python3 --version
node --version
npm --version

# Reinstall dependencies
./scripts/setup-dev.sh --skip-verify
```

---

## Script Verification

All scripts have been verified to be:
- ✅ Syntactically correct
- ✅ Functionally operational
- ✅ Properly error-handled
- ✅ Well-documented

See `SCRIPTS_VERIFICATION.md` for detailed verification report.
