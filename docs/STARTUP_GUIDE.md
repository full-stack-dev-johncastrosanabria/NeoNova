# NeoNova Startup Guide

## System Status

✅ **Documentation**: Complete and organized in `docs/` folder  
✅ **Scripts**: All verified and working  
✅ **Configuration**: Ready for deployment  
⚠️ **Python Version**: Note - System has Python 3.14 (newer than some dependencies support)

---

## Quick Start Options

### Option 1: Docker Compose (Recommended - No Python Issues)

```bash
# Navigate to project root
cd /Users/johnbenjamincastrosanabria/Desktop/NeoNova

# Copy environment template
cp .env.docker.example .env

# Edit .env with your API keys
nano .env

# Start all services
docker-compose up

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

**Advantages**:
- ✅ No local Python/Node setup needed
- ✅ Isolated environment
- ✅ Production-like setup
- ✅ Easy to scale

**Time to start**: ~2-3 minutes

---

### Option 2: Using Python 3.12 (If Available)

If you have Python 3.12 installed:

```bash
# Check Python versions
ls /usr/local/bin/python*
which python3.12

# Use Python 3.12 specifically
/usr/local/bin/python3.12 -m venv backend/venv
source backend/venv/bin/activate
pip install -e .[dev]

# Then run setup
./scripts/setup-dev.sh --skip-verify
./scripts/manage-services.sh start
```

---

### Option 3: Using Conda (Alternative)

```bash
# Create conda environment with Python 3.12
conda create -n neonova python=3.12
conda activate neonova

# Install dependencies
cd backend
pip install -e .[dev]

# Setup frontend
cd ../frontend
npm install

# Start services
../scripts/manage-services.sh start
```

---

## Recommended: Docker Compose Setup

### Step 1: Prepare Environment

```bash
cd /Users/johnbenjamincastrosanabria/Desktop/NeoNova

# Copy environment template
cp .env.docker.example .env

# Edit with your configuration
# Add your OpenAI or Azure OpenAI API key
nano .env
```

### Step 2: Start Services

```bash
# Build and start all services
docker-compose up

# Or run in background
docker-compose up -d

# Check status
docker-compose ps
```

### Step 3: Verify Services

```bash
# Check backend health
curl http://localhost:8000/health

# Check frontend
curl http://localhost:3000

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Step 4: Access Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Service URLs

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:3000 | React application |
| Backend API | http://localhost:8000 | FastAPI server |
| Swagger UI | http://localhost:8000/docs | Interactive API docs |
| ReDoc | http://localhost:8000/redoc | API documentation |
| Health Check | http://localhost:8000/health | API health status |

---

## First Steps After Starting

### 1. Create Account

```bash
# Register new user
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123",
    "display_name": "Your Name"
  }'
```

### 2. Login

```bash
# Login to get token
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

### 3. Create Conversation

```bash
# Create conversation (replace TOKEN with your token)
curl -X POST http://localhost:8000/conversations/ \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "My First Chat"}'
```

### 4. Send Message

```bash
# Send message (replace CONV_ID and TOKEN)
curl -X POST http://localhost:8000/conversations/CONV_ID/messages \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content": "Hello, NeoNova!"}'
```

---

## Managing Services

### Using Docker Compose

```bash
# Start services
docker-compose up

# Start in background
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Restart services
docker-compose restart

# Rebuild images
docker-compose build --no-cache
```

### Using Management Scripts (Local Development)

```bash
# Start all services
./scripts/manage-services.sh start

# Stop all services
./scripts/manage-services.sh stop

# Check status
./scripts/manage-services.sh status

# View logs
./scripts/manage-services.sh logs

# Restart services
./scripts/manage-services.sh restart
```

---

## Environment Configuration

### Backend (.env)

```env
# Database
DATABASE_URL=postgresql+asyncpg://neonova:neonova_dev_password@db:5432/neonova

# Authentication
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# LLM Provider
LLM_PROVIDER=openai

# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key
OPENAI_MODEL=gpt-4o-mini

# Azure OpenAI Configuration (alternative)
# AZURE_OPENAI_API_KEY=your-key
# AZURE_OPENAI_ENDPOINT=https://resource.openai.azure.com/
# AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment

# CORS
CORS_ALLOW_ORIGINS=http://localhost:3000
```

### Frontend (.env)

```env
VITE_API_URL=http://localhost:8000
```

---

## Troubleshooting Startup

### Docker Issues

```bash
# Check Docker is running
docker ps

# Start Docker (macOS)
open /Applications/Docker.app

# Check Docker Compose version
docker-compose --version

# Rebuild images
docker-compose build --no-cache

# Remove old containers
docker-compose down -v
docker-compose up
```

### Port Conflicts

```bash
# Find process using port
lsof -i :3000  # Frontend
lsof -i :8000  # Backend
lsof -i :5432  # Database

# Kill process
kill -9 <PID>

# Or change port in docker-compose.yml
```

### Database Connection

```bash
# Check PostgreSQL is running
docker-compose ps db

# Check database logs
docker-compose logs db

# Connect to database
psql -U neonova -d neonova -h localhost
```

### API Not Responding

```bash
# Check backend logs
docker-compose logs backend

# Test health endpoint
curl http://localhost:8000/health

# Check if port is listening
lsof -i :8000
```

---

## Running Tests

### With Docker

```bash
# Run backend tests in container
docker-compose exec backend pytest

# Run with coverage
docker-compose exec backend pytest --cov=src

# Run specific test
docker-compose exec backend pytest tests/unit/test_auth.py
```

### Locally (After Setup)

```bash
# Run all tests
./scripts/test-all.sh

# Backend only
./scripts/test-all.sh --backend-only

# With linting
./scripts/test-all.sh --with-lint
```

---

## Documentation

All documentation is organized in the `docs/` folder:

- **[docs/README.md](README.md)** - Documentation index
- **[docs/GETTING_STARTED.md](GETTING_STARTED.md)** - Setup guide
- **[docs/ARCHITECTURE.md](ARCHITECTURE.md)** - System design
- **[docs/API.md](API.md)** - REST API reference
- **[docs/SCRIPTS.md](SCRIPTS.md)** - Scripts guide
- **[docs/TESTING.md](TESTING.md)** - Testing guide
- **[docs/TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues

---

## Next Steps

1. **Start the system** using Docker Compose (recommended)
2. **Create an account** at http://localhost:3000
3. **Read the API documentation** at http://localhost:8000/docs
4. **Review the architecture** in `docs/ARCHITECTURE.md`
5. **Run tests** with `./scripts/test-all.sh`

---

## Support

### Check Documentation

- **Setup Issues**: See `docs/GETTING_STARTED.md`
- **API Questions**: See `docs/API.md`
- **Architecture**: See `docs/ARCHITECTURE.md`
- **Common Problems**: See `docs/TROUBLESHOOTING.md`

### Check Logs

```bash
# Docker
docker-compose logs -f

# Local
./scripts/manage-services.sh logs
```

### Check Status

```bash
# Docker
docker-compose ps

# Local
./scripts/manage-services.sh status
```

---

## System Information

**Project**: NeoNova AI Assistant  
**Status**: ✅ Ready to deploy  
**Documentation**: ✅ Complete  
**Scripts**: ✅ Verified  
**Last Updated**: May 8, 2026

---

## Quick Reference

```bash
# Docker Compose (Recommended)
docker-compose up

# Local Development
./scripts/setup-dev.sh --skip-verify
./scripts/manage-services.sh start

# Run Tests
./scripts/test-all.sh

# Check Status
./scripts/manage-services.sh status

# View Logs
./scripts/manage-services.sh logs

# Stop Services
./scripts/manage-services.sh stop
```

---

## Deployment Checklist

- [ ] Copy `.env.docker.example` to `.env`
- [ ] Add API keys to `.env`
- [ ] Run `docker-compose up`
- [ ] Verify services at http://localhost:3000
- [ ] Create test account
- [ ] Send test message
- [ ] Check API docs at http://localhost:8000/docs
- [ ] Review logs for errors
- [ ] Run tests: `./scripts/test-all.sh`

---

**Ready to start? Run: `docker-compose up`**
