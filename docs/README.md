# NeoNova Documentation

Welcome to the NeoNova AI Assistant documentation. This folder contains comprehensive guides organized by concern.

## 📚 Documentation Index

### Getting Started
- **[GETTING_STARTED.md](GETTING_STARTED.md)** - Quick start guide with setup options
  - Prerequisites and installation
  - Docker Compose setup
  - Manual setup instructions
  - Environment configuration
  - Verification steps

### Architecture & Design
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture and design patterns
  - Clean Architecture layers
  - Backend structure
  - Frontend structure
  - Data flow diagrams
  - Database schema
  - Authentication flow
  - LLM integration
  - Testing architecture
  - Deployment architecture

### API Reference
- **[API.md](API.md)** - Complete REST API documentation
  - Authentication endpoints
  - Conversation management
  - Message exchange
  - Memory management
  - Feedback collection
  - HTTP status codes
  - Request/response examples
  - Error handling

### Scripts & Automation
- **[SCRIPTS.md](SCRIPTS.md)** - Management scripts guide
  - setup-dev.sh - Environment setup
  - manage-services.sh - Service management
  - test-all.sh - Test runner
  - Common workflows
  - Log management
  - Troubleshooting scripts

### Testing
- **[TESTING.md](TESTING.md)** - Comprehensive testing guide
  - Unit tests
  - Integration tests
  - Property-based tests
  - Test fixtures
  - Coverage reports
  - Best practices
  - CI/CD integration

### Troubleshooting
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions
  - Port conflicts
  - Database issues
  - Virtual environment problems
  - API key issues
  - Performance optimization
  - Recovery procedures

---

## 🚀 Quick Start

### Option 1: Docker Compose (Easiest)

```bash
cp .env.docker.example .env
docker-compose up
# Access at http://localhost:3000
```

### Option 2: Using Scripts (Recommended for Development)

```bash
./scripts/setup-dev.sh
./scripts/manage-services.sh start
# Access at http://localhost:5173
```

### Option 3: Manual Setup

See [GETTING_STARTED.md](GETTING_STARTED.md) for detailed instructions.

---

## 📖 Documentation by Role

### For New Users
1. Start with [GETTING_STARTED.md](GETTING_STARTED.md)
2. Learn the [API.md](API.md)
3. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) if issues arise

### For Developers
1. Read [ARCHITECTURE.md](ARCHITECTURE.md)
2. Learn [SCRIPTS.md](SCRIPTS.md) for automation
3. Review [TESTING.md](TESTING.md)
4. Check [API.md](API.md) for integration

### For DevOps/Infrastructure
1. Review [ARCHITECTURE.md](ARCHITECTURE.md) - Deployment section
2. Check Docker setup in [GETTING_STARTED.md](GETTING_STARTED.md)
3. Review [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Performance section

### For QA/Testers
1. Learn [TESTING.md](TESTING.md)
2. Review [API.md](API.md) for endpoints
3. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues

---

## 🔗 Service URLs

When services are running:

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:5173 | React app (dev) |
| Frontend | http://localhost:3000 | React app (Docker) |
| Backend API | http://localhost:8000 | FastAPI server |
| API Docs | http://localhost:8000/docs | Swagger UI |
| API ReDoc | http://localhost:8000/redoc | ReDoc documentation |

---

## 📋 Common Tasks

### Start Development

```bash
./scripts/setup-dev.sh
./scripts/manage-services.sh start
```

### Run Tests

```bash
./scripts/test-all.sh
./scripts/test-all.sh --with-lint
```

### Check Service Status

```bash
./scripts/manage-services.sh status
```

### View Logs

```bash
./scripts/manage-services.sh logs
./scripts/manage-services.sh logs backend
./scripts/manage-services.sh logs frontend
```

### Stop Services

```bash
./scripts/manage-services.sh stop
```

---

## 🏗️ Project Structure

```
NeoNova/
├── docs/                    # Documentation (this folder)
│   ├── README.md           # This file
│   ├── GETTING_STARTED.md  # Setup guide
│   ├── ARCHITECTURE.md     # System design
│   ├── API.md              # API reference
│   ├── SCRIPTS.md          # Scripts guide
│   ├── TESTING.md          # Testing guide
│   └── TROUBLESHOOTING.md  # Troubleshooting
├── backend/                # FastAPI backend
│   ├── src/                # Source code
│   ├── tests/              # Test suite
│   ├── alembic/            # Database migrations
│   └── pyproject.toml      # Dependencies
├── frontend/               # React frontend
│   ├── src/                # Source code
│   ├── package.json        # Dependencies
│   └── vite.config.ts      # Build config
├── scripts/                # Management scripts
│   ├── setup-dev.sh        # Setup script
│   ├── manage-services.sh  # Service management
│   └── test-all.sh         # Test runner
└── docker-compose.yml      # Docker configuration
```

---

## 🔐 Environment Configuration

### Backend (.env)

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/neonova
SECRET_KEY=your-secret-key
OPENAI_API_KEY=sk-your-key
LLM_PROVIDER=openai
```

### Frontend (.env)

```env
VITE_API_URL=http://localhost:8000
```

See [GETTING_STARTED.md](GETTING_STARTED.md) for complete configuration.

---

## 🧪 Testing

```bash
# All tests
./scripts/test-all.sh

# Backend only
./scripts/test-all.sh --backend-only

# With linting
./scripts/test-all.sh --with-lint
```

See [TESTING.md](TESTING.md) for detailed testing guide.

---

## 🐛 Troubleshooting

Common issues and solutions are documented in [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

Quick fixes:

```bash
# Port already in use
lsof -i :8000
kill -9 <PID>

# Database connection failed
psql -U neonova -d neonova -c "SELECT 1"

# Virtual environment issues
rm -rf backend/venv
./scripts/setup-dev.sh --skip-verify
```

---

## 📞 Getting Help

1. **Check Documentation**: Search relevant docs
2. **Check Logs**: `./scripts/manage-services.sh logs`
3. **Check Status**: `./scripts/manage-services.sh status`
4. **Troubleshooting**: See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
5. **GitHub Issues**: Create an issue with details

---

## 🔄 Workflow

### Development Workflow

```bash
# 1. Setup (first time)
./scripts/setup-dev.sh

# 2. Start services
./scripts/manage-services.sh start

# 3. Make changes
# Edit code in backend/ or frontend/

# 4. Run tests
./scripts/test-all.sh

# 5. Commit changes
git add .
git commit -m "feat: description"
git push
```

### Deployment Workflow

```bash
# 1. Build Docker images
docker-compose build

# 2. Start services
docker-compose up

# 3. Verify health
curl http://localhost:8000/health
curl http://localhost:3000
```

---

## 📚 Additional Resources

- **Main README**: See `../README.md`
- **Scripts Verification**: See `../SCRIPTS_VERIFICATION.md`
- **Scripts Quick Reference**: See `../SCRIPTS_QUICK_REFERENCE.md`
- **GitHub Repository**: https://github.com/yourusername/neonova
- **OpenAI API**: https://platform.openai.com/docs
- **FastAPI**: https://fastapi.tiangolo.com/
- **React**: https://react.dev/

---

## 📝 Documentation Maintenance

This documentation is organized by concern:

- **GETTING_STARTED.md** - Setup and installation
- **ARCHITECTURE.md** - System design and structure
- **API.md** - REST API reference
- **SCRIPTS.md** - Automation and management
- **TESTING.md** - Testing strategies and practices
- **TROUBLESHOOTING.md** - Common issues and solutions

Each document is self-contained but cross-references other docs as needed.

---

## ✅ Verification

All documentation has been verified to be:
- ✅ Accurate and up-to-date
- ✅ Complete and comprehensive
- ✅ Well-organized and easy to navigate
- ✅ Includes practical examples
- ✅ Covers common issues

**Last Updated**: May 8, 2026  
**Status**: Complete and verified
