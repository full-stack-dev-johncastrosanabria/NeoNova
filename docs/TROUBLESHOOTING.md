# NeoNova Troubleshooting Guide

## Common Issues and Solutions

### Port Already in Use

**Problem**: Services won't start because ports are already in use

```
Error: Address already in use
Port 8000 is already in use by another process
```

**Solution**:

```bash
# Find process using port
lsof -i :8000  # Backend
lsof -i :5173  # Frontend

# Kill the process
kill -9 <PID>

# Or restart services
./scripts/manage-services.sh restart
```

---

### Database Connection Failed

**Problem**: Backend can't connect to PostgreSQL

```
Error: could not connect to server: Connection refused
```

**Solution**:

```bash
# Check PostgreSQL is running
psql -U neonova -d neonova -c "SELECT 1"

# Start PostgreSQL (macOS)
brew services start postgresql

# Start PostgreSQL (Linux)
sudo systemctl start postgresql

# Create database if missing
createdb neonova_dev

# Run migrations
cd backend
source venv/bin/activate
alembic upgrade head
```

---

### Virtual Environment Issues

**Problem**: Python packages not found or wrong version

```
ModuleNotFoundError: No module named 'fastapi'
```

**Solution**:

```bash
# Verify virtual environment is activated
which python  # Should show path in venv/

# Recreate virtual environment
rm -rf backend/venv
python3 -m venv backend/venv
source backend/venv/bin/activate

# Reinstall dependencies
pip install -e .[dev]
```

---

### Node Modules Issues

**Problem**: Frontend dependencies not found

```
Error: Cannot find module 'react'
```

**Solution**:

```bash
# Reinstall node modules
cd frontend
rm -rf node_modules package-lock.json
npm install

# Clear npm cache
npm cache clean --force
npm install
```

---

### Environment File Missing

**Problem**: `.env` file not found

```
Error: .env file not found
```

**Solution**:

```bash
# Copy template
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Edit files with your configuration
nano backend/.env
nano frontend/.env
```

---

### API Key Issues

**Problem**: LLM provider returns authentication error

```
Error: Invalid API key
Error: 401 Unauthorized
```

**Solution**:

```bash
# Verify API key in .env
cat backend/.env | grep OPENAI_API_KEY

# Check API key format
# OpenAI: Should start with 'sk-'
# Azure: Should be a long string

# Test API key
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
  https://api.openai.com/v1/models

# Get new API key
# OpenAI: https://platform.openai.com/api-keys
# Azure: https://portal.azure.com
```

---

### Tests Failing

**Problem**: Tests fail with errors

```
FAILED tests/unit/test_auth.py::test_hash_password
```

**Solution**:

```bash
# Run with verbose output
pytest -v

# Show print statements
pytest -s

# Stop on first failure
pytest -x

# Run specific test
pytest tests/unit/test_auth.py::test_hash_password -v

# Check test database
rm -rf backend/test.db
pytest
```

---

### Frontend Build Issues

**Problem**: Frontend won't build or start

```
Error: ENOENT: no such file or directory
```

**Solution**:

```bash
# Clear build artifacts
cd frontend
rm -rf dist node_modules .vite

# Reinstall dependencies
npm install

# Try building again
npm run build

# Check Node.js version
node --version  # Should be 18+
```

---

### Backend Won't Start

**Problem**: Backend service fails to start

```
Error: Failed to start backend
```

**Solution**:

```bash
# Check logs
./scripts/manage-services.sh logs backend

# Verify Python version
python3 --version  # Should be 3.12+

# Check virtual environment
source backend/venv/bin/activate
which python

# Reinstall dependencies
pip install -e .[dev]

# Try starting manually
cd backend
uvicorn src.main:app --reload
```

---

### Frontend Won't Start

**Problem**: Frontend service fails to start

```
Error: Failed to start frontend
```

**Solution**:

```bash
# Check logs
./scripts/manage-services.sh logs frontend

# Verify Node.js version
node --version  # Should be 18+

# Check npm version
npm --version  # Should be 8+

# Reinstall dependencies
cd frontend
npm install

# Try starting manually
npm run dev
```

---

### Health Check Failing

**Problem**: Services start but health checks fail

```
Backend health check failed after 30 attempts
```

**Solution**:

```bash
# Check service logs
./scripts/manage-services.sh logs backend

# Test health endpoint manually
curl http://localhost:8000/health

# Check if port is actually listening
lsof -i :8000

# Increase health check timeout
# Edit manage-services.sh and increase max_attempts
```

---

### Database Migrations Failed

**Problem**: Alembic migrations fail

```
Error: Can't locate revision identified by 'abc123'
```

**Solution**:

```bash
# Check migration status
cd backend
alembic current

# View migration history
alembic history

# Downgrade to previous version
alembic downgrade -1

# Upgrade to latest
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "Description"
```

---

### CORS Issues

**Problem**: Frontend can't access backend API

```
Error: Access to XMLHttpRequest blocked by CORS policy
```

**Solution**:

```bash
# Check CORS configuration in backend/.env
cat backend/.env | grep CORS_ALLOW_ORIGINS

# Should include frontend URL
CORS_ALLOW_ORIGINS=http://localhost:5173

# Restart backend
./scripts/manage-services.sh restart
```

---

### Authentication Token Issues

**Problem**: Token validation fails

```
Error: 401 Unauthorized
Error: Invalid token
```

**Solution**:

```bash
# Check SECRET_KEY in backend/.env
cat backend/.env | grep SECRET_KEY

# Token should be in Authorization header
Authorization: Bearer <token>

# Check token expiration
# Default: 30 minutes

# Get new token by logging in again
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password"}'
```

---

### Memory Issues

**Problem**: System runs out of memory

```
Error: MemoryError
Error: Cannot allocate memory
```

**Solution**:

```bash
# Check memory usage
top

# Stop unnecessary services
./scripts/manage-services.sh stop

# Clear caches
npm cache clean --force
pip cache purge

# Restart services
./scripts/manage-services.sh start
```

---

### Disk Space Issues

**Problem**: Disk is full

```
Error: No space left on device
```

**Solution**:

```bash
# Check disk usage
df -h

# Clean up logs
rm -rf logs/*

# Clean up node_modules
rm -rf frontend/node_modules

# Clean up Python cache
find . -type d -name __pycache__ -exec rm -r {} +
find . -type f -name "*.pyc" -delete

# Clean up Docker (if using)
docker system prune
```

---

### Slow Performance

**Problem**: Application is slow

**Solution**:

```bash
# Check system resources
top
free -h

# Check database performance
psql -U neonova -d neonova -c "SELECT * FROM pg_stat_statements LIMIT 10;"

# Check API response times
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/health

# Enable query logging
# Add to backend/.env:
# SQLALCHEMY_ECHO=true

# Profile code
# Use Python profiler:
# python -m cProfile -s cumulative src/main.py
```

---

### Dependency Conflicts

**Problem**: Dependency version conflicts

```
Error: Conflicting dependencies
```

**Solution**:

```bash
# Backend
cd backend
pip list  # Check installed versions
pip install --upgrade pip
pip install -e .[dev] --upgrade

# Frontend
cd frontend
npm outdated  # Check for outdated packages
npm update
```

---

### Git Issues

**Problem**: Git conflicts or issues

```
Error: merge conflict
```

**Solution**:

```bash
# Check status
git status

# Resolve conflicts
# Edit conflicting files
git add .
git commit -m "Resolve conflicts"

# Or abort merge
git merge --abort
```

---

### Docker Issues

**Problem**: Docker containers won't start

```
Error: Cannot connect to Docker daemon
```

**Solution**:

```bash
# Check Docker is running
docker ps

# Start Docker (macOS)
open /Applications/Docker.app

# Start Docker (Linux)
sudo systemctl start docker

# Check Docker Compose
docker-compose --version

# Rebuild images
docker-compose build --no-cache

# Remove old containers
docker-compose down -v
docker-compose up
```

---

## Getting Help

### Check Logs

```bash
# Backend logs
./scripts/manage-services.sh logs backend

# Frontend logs
./scripts/manage-services.sh logs frontend

# All logs
./scripts/manage-services.sh logs
```

### Check Status

```bash
# Service status
./scripts/manage-services.sh status

# Database status
psql -U neonova -d neonova -c "SELECT 1"

# API health
curl http://localhost:8000/health
```

### Debug Mode

```bash
# Backend debug
cd backend
export DEBUG=true
uvicorn src.main:app --reload --log-level debug

# Frontend debug
cd frontend
npm run dev -- --debug
```

### Collect Information

When reporting issues, include:

1. **Error message** - Full error text
2. **Steps to reproduce** - How to trigger the issue
3. **System info** - OS, Python version, Node version
4. **Logs** - Relevant log output
5. **Configuration** - Environment variables (without secrets)

### Resources

- **Documentation**: See `docs/` folder
- **GitHub Issues**: https://github.com/yourusername/neonova/issues
- **API Docs**: http://localhost:8000/docs
- **Architecture**: See `docs/ARCHITECTURE.md`

---

## Performance Optimization

### Backend Optimization

```python
# Use connection pooling
# Already configured in database.py

# Add caching
# Future: Redis integration

# Optimize queries
# Use select() with specific columns
# Add indexes on frequently queried columns
```

### Frontend Optimization

```bash
# Build optimization
npm run build

# Check bundle size
npm run build -- --analyze

# Enable compression
# Already configured in nginx.conf
```

### Database Optimization

```sql
-- Check slow queries
SELECT * FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 10;

-- Add indexes
CREATE INDEX idx_user_email ON users(email);
CREATE INDEX idx_conversation_user_id ON conversations(user_id);
CREATE INDEX idx_message_conversation_id ON messages(conversation_id);
CREATE INDEX idx_memory_user_id ON memories(user_id);
CREATE INDEX idx_memory_is_active ON memories(is_active);
```

---

## Monitoring

### Health Checks

```bash
# Backend health
curl http://localhost:8000/health

# Frontend health
curl http://localhost:5173

# Database health
psql -U neonova -d neonova -c "SELECT 1"
```

### Metrics

```bash
# API response time
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/docs

# Database connections
psql -U neonova -d neonova -c "SELECT count(*) FROM pg_stat_activity;"

# System resources
top
free -h
df -h
```

---

## Recovery Procedures

### Full Reset

```bash
# Stop services
./scripts/manage-services.sh stop

# Remove all data
rm -rf backend/venv
rm -rf frontend/node_modules
rm -rf logs/*
dropdb neonova_dev

# Reinstall
./scripts/setup-dev.sh

# Start services
./scripts/manage-services.sh start
```

### Database Recovery

```bash
# Backup database
pg_dump neonova_dev > backup.sql

# Restore database
psql neonova_dev < backup.sql

# Reset migrations
cd backend
alembic downgrade base
alembic upgrade head
```

### Code Recovery

```bash
# Discard local changes
git checkout .

# Reset to last commit
git reset --hard HEAD

# Reset to specific commit
git reset --hard <commit-hash>
```
