# NeoNova Testing Guide

## Overview

NeoNova includes comprehensive testing at multiple levels:

1. **Unit Tests** - Test individual components in isolation
2. **Integration Tests** - Test complete workflows with real database
3. **Property-Based Tests** - Verify invariants across many inputs

## Running Tests

### Quick Start

```bash
# Run all tests
./scripts/test-all.sh

# Backend tests only
./scripts/test-all.sh --backend-only

# Frontend tests only
./scripts/test-all.sh --frontend-only

# With linting
./scripts/test-all.sh --with-lint
```

### Manual Test Execution

#### Backend Tests

```bash
cd backend

# All tests
pytest

# Specific test file
pytest tests/unit/test_auth.py

# Specific test
pytest tests/unit/test_auth.py::test_hash_password

# With coverage
pytest --cov=src --cov-report=html

# Verbose output
pytest -v

# Stop on first failure
pytest -x

# Show print statements
pytest -s
```

#### Frontend Tests

```bash
cd frontend

# Run tests
npm test

# Watch mode
npm test -- --watch

# Coverage
npm test -- --coverage
```

---

## Test Structure

### Backend Tests

```
backend/tests/
├── conftest.py                          # Shared fixtures
├── unit/
│   ├── test_entities.py                 # Domain entity tests
│   ├── test_auth_service.py             # Auth service tests
│   ├── test_memory_service.py           # Memory service tests
│   └── test_agent_service.py            # Agent service tests
├── integration/
│   ├── conftest.py                      # Integration test fixtures
│   ├── test_auth_flow.py                # Authentication flow tests
│   ├── test_message_flow.py             # Message exchange tests
│   └── test_feedback_memory_flow.py     # Feedback and memory tests
└── properties/
    ├── test_domain_properties.py        # Domain entity properties
    ├── test_auth_properties.py          # Authentication properties
    ├── test_memory_agent_properties.py  # Memory and agent properties
    ├── test_conversation_message_properties.py  # Conversation properties
    └── test_feedback_llm_properties.py  # Feedback and LLM properties
```

### Frontend Tests

```
frontend/src/
├── __tests__/
│   ├── components/
│   │   ├── Chat.test.tsx
│   │   ├── ConversationList.test.tsx
│   │   └── FeedbackModal.test.tsx
│   ├── pages/
│   │   ├── LoginPage.test.tsx
│   │   └── ChatPage.test.tsx
│   └── services/
│       └── api.test.ts
```

---

## Unit Tests

### Purpose

Test individual components in isolation using mocks for dependencies.

### Example: Entity Validation

```python
def test_user_email_validation():
    """Test that User entity validates email format"""
    with pytest.raises(ValueError, match="Invalid email format"):
        User(
            id=uuid4(),
            email="not-an-email",
            display_name="Test User",
            password_hash="hash",
            created_at=datetime.utcnow()
        )

def test_user_display_name_validation():
    """Test that User entity validates display name"""
    with pytest.raises(ValueError, match="Display name cannot be empty"):
        User(
            id=uuid4(),
            email="user@example.com",
            display_name="",
            password_hash="hash",
            created_at=datetime.utcnow()
        )
```

### Example: Service Testing

```python
@pytest.mark.asyncio
async def test_hash_password():
    """Test password hashing"""
    auth_service = AuthService()
    password = "securepassword123"
    
    hash1 = auth_service.hash_password(password)
    hash2 = auth_service.hash_password(password)
    
    # Hashes should be different (salt)
    assert hash1 != hash2
    
    # Both should verify
    assert auth_service.verify_password(password, hash1)
    assert auth_service.verify_password(password, hash2)
```

---

## Integration Tests

### Purpose

Test complete workflows with real database and all dependencies.

### Example: Authentication Flow

```python
@pytest.mark.asyncio
async def test_register_and_login_flow(test_client: AsyncClient):
    """Test complete registration and login flow"""
    
    # 1. Register user
    register_response = await test_client.post(
        "/auth/register",
        json={
            "email": "user@example.com",
            "password": "securepassword123",
            "display_name": "Test User"
        }
    )
    assert register_response.status_code == 201
    user_data = register_response.json()
    assert user_data["email"] == "user@example.com"
    
    # 2. Login with correct credentials
    login_response = await test_client.post(
        "/auth/login",
        json={
            "email": "user@example.com",
            "password": "securepassword123"
        }
    )
    assert login_response.status_code == 200
    login_data = login_response.json()
    assert "token" in login_data
    
    # 3. Use token to access protected endpoint
    protected_response = await test_client.get(
        "/memories/",
        headers={"Authorization": f"Bearer {login_data['token']}"}
    )
    assert protected_response.status_code == 200
```

### Example: Message Flow

```python
@pytest.mark.asyncio
async def test_send_message_flow(
    test_client: AsyncClient,
    test_user_token: str,
    test_conversation
):
    """Test complete message sending flow"""
    
    # Send message
    response = await test_client.post(
        f"/conversations/{test_conversation.id}/messages",
        json={"content": "Hello, assistant!"},
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    
    assert response.status_code == 200
    messages = response.json()
    
    # Should return two messages: user and assistant
    assert len(messages) == 2
    assert messages[0]["role"] == "user"
    assert messages[0]["content"] == "Hello, assistant!"
    assert messages[1]["role"] == "assistant"
    assert len(messages[1]["content"]) > 0
```

---

## Property-Based Tests

### Purpose

Use Hypothesis to generate many test cases and verify invariants hold.

### Example: Domain Properties

```python
from hypothesis import given, strategies as st

@given(st.text().filter(lambda x: '@' not in x))
def test_user_email_must_contain_at_symbol(invalid_email: str):
    """Property: User email must contain '@' symbol"""
    with pytest.raises(ValueError):
        User(
            id=uuid4(),
            email=invalid_email,
            display_name="Test",
            password_hash="hash",
            created_at=datetime.utcnow()
        )

@given(st.integers(min_value=1, max_value=4))
def test_memory_importance_valid_range(importance: int):
    """Property: Memory importance must be 1-4"""
    memory = Memory(
        id=uuid4(),
        user_id=uuid4(),
        type=MemoryType.PREFERENCE,
        content="Test",
        importance=MemoryImportance(importance),
        source_message_id=None,
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    assert 1 <= memory.importance.value <= 4
```

### Example: Service Properties

```python
@given(
    st.lists(
        st.tuples(
            st.sampled_from(list(MemoryImportance)),
            st.datetimes()
        ),
        min_size=2,
        max_size=10
    )
)
async def test_memories_sorted_by_importance_then_recency(
    importance_datetime_pairs
):
    """Property: Memories are sorted by importance desc, then recency desc"""
    # Create memories with given importance and datetime
    memories = [
        Memory(
            id=uuid4(),
            user_id=uuid4(),
            type=MemoryType.PREFERENCE,
            content=f"Memory {i}",
            importance=importance,
            source_message_id=None,
            is_active=True,
            created_at=created_at,
            updated_at=created_at
        )
        for i, (importance, created_at) in enumerate(importance_datetime_pairs)
    ]
    
    # Mock repository
    mock_repo = AsyncMock()
    mock_repo.find_active_by_user.return_value = memories
    
    # Get sorted memories
    service = MemoryService(mock_repo)
    result = await service.get_active_memories(uuid4())
    
    # Verify sorting
    for i in range(len(result) - 1):
        current = result[i]
        next_memory = result[i + 1]
        
        if current.importance.value != next_memory.importance.value:
            assert current.importance.value > next_memory.importance.value
        else:
            assert current.created_at >= next_memory.created_at
```

---

## Test Fixtures

### Backend Fixtures

```python
# conftest.py

@pytest.fixture
async def test_db_session():
    """Provide test database session"""
    # Create in-memory SQLite database
    # Run migrations
    # Yield session
    # Cleanup

@pytest.fixture
async def test_client(test_db_session):
    """Provide test HTTP client"""
    # Create FastAPI app
    # Override database dependency
    # Create AsyncClient
    # Yield client

@pytest.fixture
async def test_user(test_db_session):
    """Create test user in database"""
    # Create user with known credentials
    # Return user entity

@pytest.fixture
async def test_user_token(test_user):
    """Generate JWT token for test user"""
    # Create token for test_user
    # Return token string

@pytest.fixture
async def test_conversation(test_db_session, test_user):
    """Create test conversation"""
    # Create conversation for test_user
    # Return conversation entity
```

---

## Coverage Reports

### Generate Coverage Report

```bash
cd backend

# Generate HTML report
pytest --cov=src --cov-report=html

# View report
open htmlcov/index.html
```

### Coverage Goals

- **Overall**: 80%+ coverage
- **Domain Layer**: 95%+ (critical business logic)
- **Application Layer**: 90%+ (use cases and services)
- **Infrastructure Layer**: 70%+ (database and external services)
- **API Layer**: 85%+ (routes and schemas)

---

## Continuous Integration

### GitHub Actions (Example)

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.12'
      
      - name: Install dependencies
        run: |
          cd backend
          pip install -e .[dev]
      
      - name: Run tests
        run: |
          cd backend
          pytest --cov=src
      
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

---

## Best Practices

### 1. Test Naming

```python
# Good: Describes what is being tested and expected outcome
def test_user_creation_with_valid_email_succeeds():
    pass

# Bad: Vague name
def test_user():
    pass
```

### 2. Arrange-Act-Assert Pattern

```python
def test_send_message():
    # Arrange: Set up test data
    user = create_test_user()
    conversation = create_test_conversation(user)
    
    # Act: Perform the action
    result = send_message(conversation, "Hello")
    
    # Assert: Verify the outcome
    assert len(result) == 2
    assert result[0]["role"] == "user"
    assert result[1]["role"] == "assistant"
```

### 3. Use Fixtures for Setup

```python
# Good: Reusable fixture
@pytest.fixture
def test_user():
    return create_user(email="test@example.com")

def test_login(test_user):
    result = login(test_user.email, "password")
    assert result.success

# Bad: Repeated setup
def test_login():
    user = create_user(email="test@example.com")
    result = login(user.email, "password")
    assert result.success
```

### 4. Test One Thing

```python
# Good: Tests one behavior
def test_password_hashing_produces_different_hashes():
    hash1 = hash_password("password")
    hash2 = hash_password("password")
    assert hash1 != hash2

# Bad: Tests multiple things
def test_password_hashing():
    hash1 = hash_password("password")
    hash2 = hash_password("password")
    assert hash1 != hash2
    assert verify_password("password", hash1)
    assert not verify_password("wrong", hash1)
```

---

## Troubleshooting

### Tests Failing

```bash
# Run with verbose output
pytest -v

# Show print statements
pytest -s

# Stop on first failure
pytest -x

# Run specific test
pytest tests/unit/test_auth.py::test_hash_password -v
```

### Database Issues

```bash
# Check database connection
psql -U neonova -d neonova -c "SELECT 1"

# Reset test database
rm -rf backend/test.db
pytest
```

### Import Errors

```bash
# Verify virtual environment is activated
source backend/venv/bin/activate

# Reinstall dependencies
pip install -e .[dev]

# Check Python path
python -c "import sys; print(sys.path)"
```

---

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [Hypothesis Documentation](https://hypothesis.readthedocs.io/)
- [SQLAlchemy Testing](https://docs.sqlalchemy.org/en/20/faq/testing.html)
- [FastAPI Testing](https://fastapi.tiangolo.com/advanced/testing-dependencies/)
