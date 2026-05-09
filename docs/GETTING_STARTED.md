# Getting Started with NeoNova

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python** 3.12 or later
- **Node.js** 18 or later
- **PostgreSQL** 14 or later
- **Docker** 20.10+ and **Docker Compose** 2.0+ (optional, for containerized setup)
- **Git** for version control

### Verify Installation

```bash
python3 --version      # Should be 3.12+
node --version         # Should be 18+
npm --version          # Should be 8+
psql --version         # Should be 14+
```

## Quick Start (Recommended)

### Option 1: Using Docker Compose (Easiest)

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/neonova.git
cd neonova

# 2. Copy environment template
cp .env.docker.example .env

# 3. Edit .env with your API keys
# Add your OpenAI or Azure OpenAI credentials

# 4. Start all services
docker-compose up

# 5. Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2: Using Setup Script (Recommended for Development)

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/neonova.git
cd neonova

# 2. Run setup script
./scripts/setup-dev.sh

# 3. Edit environment files
# backend/.env - Add database and API credentials
# frontend/.env - Configure API URL

# 4. Start services
./scripts/manage-services.sh start

# 5. Access the application
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
```

### Option 3: Manual Setup

#### Backend Setup

```bash
# 1. Navigate to backend
cd backend

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -e .[dev]

# 4. Configure environment
cp .env.example .env
# Edit .env with your configuration

# 5. Setup database
createdb neonova_dev
alembic upgrade head

# 6. Start backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

```bash
# 1. Navigate to frontend
cd frontend

# 2. Install dependencies
npm install

# 3. Configure environment
cp .env.example .env
# Edit .env with backend URL

# 4. Start frontend
npm run dev
```

## Environment Configuration

### Backend (.env)

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/neonova

# Authentication
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# LLM Provider (choose one)
LLM_PROVIDER=openai

# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key
OPENAI_MODEL=gpt-4o-mini

# Azure OpenAI Configuration (alternative)
# AZURE_OPENAI_API_KEY=your-key
# AZURE_OPENAI_ENDPOINT=https://resource.openai.azure.com/
# AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment

# CORS
CORS_ALLOW_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Frontend (.env)

```env
VITE_API_URL=http://localhost:8000
```

## Verify Installation

### Check Backend

```bash
curl http://localhost:8000/health
# Should return: {"status": "ok"}
```

### Check Frontend

```bash
# Open in browser: http://localhost:5173
# Should see login page
```

### Check API Documentation

```bash
# Open in browser: http://localhost:8000/docs
# Should see Swagger UI with all endpoints
```

## Next Steps

1. **Read the Architecture Guide**: See `docs/ARCHITECTURE.md`
2. **Learn the API**: See `docs/API.md`
3. **Run Tests**: See `docs/TESTING.md`
4. **Manage Services**: See `docs/SCRIPTS.md`
5. **Troubleshoot Issues**: See `docs/TROUBLESHOOTING.md`

## Common Issues

### Port Already in Use

```bash
# Find process using port
lsof -i :8000  # Backend
lsof -i :5173  # Frontend

# Kill process
kill -9 <PID>
```

### Database Connection Failed

```bash
# Check PostgreSQL is running
psql -U neonova -d neonova -c "SELECT 1"

# Create database if missing
createdb neonova_dev
```

### Virtual Environment Issues

```bash
# Recreate virtual environment
rm -rf backend/venv
python3 -m venv backend/venv
source backend/venv/bin/activate
pip install -e .[dev]
```

## Getting Help

- Check `docs/TROUBLESHOOTING.md` for common issues
- Review `docs/FAQ.md` for frequently asked questions
- Check GitHub Issues for similar problems
- Create a new issue with detailed description

## Next: Start the System

Once setup is complete, proceed to `docs/SCRIPTS.md` to learn how to manage services.
