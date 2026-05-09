# NeoNova Architecture

## Overview

NeoNova follows **Clean Architecture** principles with clear separation of concerns across four layers:

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

## Backend Architecture

### Directory Structure

```
backend/
├── src/
│   ├── api/                          # API Layer
│   │   ├── routes/                   # Endpoint handlers
│   │   ├── schemas/                  # Pydantic request/response models
│   │   ├── auth.py                   # Authentication middleware
│   │   └── dependencies.py           # Dependency injection
│   │
│   ├── application/                  # Application Layer
│   │   ├── use_cases/                # Business logic workflows
│   │   ├── services/                 # Cross-cutting services
│   │   ├── interfaces/               # Abstract interfaces
│   │   ├── dtos/                     # Data transfer objects
│   │   └── config.py                 # Configuration management
│   │
│   ├── domain/                       # Domain Layer
│   │   ├── entities/                 # Business entities
│   │   ├── enums.py                  # Domain enumerations
│   │   └── value_objects/            # Value objects
│   │
│   ├── infrastructure/               # Infrastructure Layer
│   │   ├── repositories/             # Data access implementations
│   │   ├── models/                   # SQLAlchemy ORM models
│   │   ├── llm_providers/            # LLM integrations
│   │   └── database.py               # Database configuration
│   │
│   └── main.py                       # FastAPI application entry point
│
├── tests/
│   ├── unit/                         # Unit tests
│   ├── integration/                  # Integration tests
│   └── properties/                   # Property-based tests
│
├── alembic/                          # Database migrations
├── pyproject.toml                    # Python dependencies
└── Dockerfile                        # Container image
```

### Layer Responsibilities

#### API Layer
- **Routes**: HTTP endpoint handlers
- **Schemas**: Request/response validation with Pydantic
- **Auth**: JWT token validation and user extraction
- **Dependencies**: Dependency injection for use cases and services

#### Application Layer
- **Use Cases**: Business logic workflows (register, login, send message, etc.)
- **Services**: Cross-cutting concerns (auth, memory, agent orchestration)
- **Interfaces**: Abstract contracts for repositories and LLM providers
- **DTOs**: Data transfer objects for use case inputs/outputs

#### Domain Layer
- **Entities**: Core business objects (User, Conversation, Message, Memory, Feedback)
- **Enums**: Domain enumerations (MessageRole, MemoryType, MemoryImportance)
- **Value Objects**: Immutable objects representing domain concepts

#### Infrastructure Layer
- **Repositories**: Data access implementations (User, Conversation, Message, Memory, Feedback)
- **Models**: SQLAlchemy ORM models mapping to database tables
- **LLM Providers**: Adapters for OpenAI and Azure OpenAI APIs
- **Database**: Connection pooling, session management, migrations

## Frontend Architecture

### Directory Structure

```
frontend/
├── src/
│   ├── components/                   # Reusable React components
│   │   ├── ConversationList.tsx       # Conversation sidebar
│   │   ├── Chat.tsx                   # Message display and input
│   │   └── FeedbackModal.tsx          # Feedback form
│   │
│   ├── pages/                        # Page components
│   │   ├── LoginPage.tsx             # Authentication page
│   │   └── ChatPage.tsx              # Main chat interface
│   │
│   ├── services/                     # API client
│   │   └── api.ts                    # Axios-based API client
│   │
│   ├── types/                        # TypeScript interfaces
│   │   └── index.ts                  # Type definitions
│   │
│   ├── App.tsx                       # Main app component
│   └── main.tsx                      # Entry point
│
├── package.json                      # Node dependencies
├── vite.config.ts                    # Vite configuration
└── Dockerfile                        # Container image
```

### Component Hierarchy

```
App
├── LoginPage
│   ├── Email input
│   ├── Password input
│   └── Register/Login toggle
│
└── ChatPage
    ├── ConversationList
    │   ├── Conversation items
    │   └── New conversation button
    │
    └── Chat
        ├── Message list
        ├── Message input
        └── Feedback button
            └── FeedbackModal
```

## Data Flow

### Message Exchange Flow

```
User Input
    ↓
Frontend (Chat.tsx)
    ↓
API Client (api.ts)
    ↓
Backend Route (POST /conversations/{id}/messages)
    ↓
SendMessageUseCase
    ├─→ Get active memories (MemoryService)
    ├─→ Get conversation history
    ├─→ Build prompt (AgentService)
    └─→ Call LLM Provider
        ↓
    Save user message
    Save assistant message
    Update conversation timestamp
    ↓
Response with both messages
    ↓
Frontend displays messages
```

### Memory Context Flow

```
User Feedback with Correction
    ↓
CreateFeedbackUseCase
    ├─→ Save feedback
    └─→ Extract memory (MemoryService)
        ↓
    Create Memory entity
    Save to repository
    ↓
Next Message Request
    ↓
SendMessageUseCase
    ├─→ Get active memories
    │   (sorted by importance, then recency)
    │
    ├─→ Format memories (top 5)
    │
    └─→ Include in prompt context
        ↓
    LLM generates response with memory context
```

## Key Design Patterns

### 1. Repository Pattern
- Abstracts data access
- Enables testing with mocks
- Supports multiple data sources

### 2. Use Case Pattern
- Encapsulates business logic
- Coordinates between repositories and services
- Handles validation and error cases

### 3. Dependency Injection
- Loose coupling between layers
- Easy to test with mocks
- Flexible configuration

### 4. Service Layer
- Cross-cutting concerns (auth, memory, agent)
- Reusable business logic
- Separation from use cases

### 5. DTO Pattern
- Type-safe data transfer
- Validation at boundaries
- Decouples internal and external representations

## Database Schema

### Core Tables

```
users
├── id (UUID, PK)
├── email (String, unique)
├── display_name (String)
├── password_hash (String)
└── created_at (DateTime)

conversations
├── id (UUID, PK)
├── user_id (UUID, FK → users)
├── title (String)
├── created_at (DateTime)
└── updated_at (DateTime)

messages
├── id (UUID, PK)
├── conversation_id (UUID, FK → conversations)
├── role (Enum: user, assistant, system)
├── content (Text)
├── metadata_json (JSONB)
└── created_at (DateTime)

memories
├── id (UUID, PK)
├── user_id (UUID, FK → users)
├── type (Enum: preference, fact, instruction, correction, project_context)
├── content (Text)
├── importance (Integer: 1-4)
├── source_message_id (UUID, nullable)
├── is_active (Boolean)
├── created_at (DateTime)
└── updated_at (DateTime)

feedback
├── id (UUID, PK)
├── message_id (UUID, FK → messages, unique)
├── user_id (UUID, FK → users)
├── rating (Integer: 1-5, nullable)
├── comment (Text, nullable)
├── correction (Text, nullable)
└── created_at (DateTime)
```

### Future Tables (Prepared)

```
documents
├── id (UUID, PK)
├── user_id (UUID, FK → users)
├── title (String)
├── content (Text)
└── created_at (DateTime)

document_chunks
├── id (UUID, PK)
├── document_id (UUID, FK → documents)
├── content (Text)
├── embedding (Vector)
└── created_at (DateTime)

tool_executions
├── id (UUID, PK)
├── user_id (UUID, FK → users)
├── tool_name (String)
├── input (JSONB)
├── output (JSONB)
└── created_at (DateTime)
```

## Authentication Flow

```
User Registration
    ↓
RegisterUserUseCase
    ├─→ Validate email format
    ├─→ Check duplicate email
    ├─→ Hash password (bcrypt)
    └─→ Save User entity
        ↓
    Return user data (no password_hash)

User Login
    ↓
LoginUseCase
    ├─→ Find user by email
    ├─→ Verify password hash
    └─→ Generate JWT token
        ↓
    Return token + user data

Protected Request
    ↓
Auth Middleware
    ├─→ Extract Bearer token
    ├─→ Decode JWT
    ├─→ Validate expiration
    └─→ Fetch user from database
        ↓
    Inject user into route handler
```

## LLM Integration

### Provider Interface

```python
class ILLMProvider:
    async def generate_completion(
        messages: List[LLMMessage],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> LLMResponse
    
    async def generate_embedding(text: str) -> List[float]
```

### Supported Providers

1. **OpenAI**
   - Uses `openai.AsyncOpenAI` client
   - Configurable model (gpt-4, gpt-3.5-turbo, etc.)
   - Supports embeddings for future RAG

2. **Azure OpenAI**
   - Uses `openai.AsyncAzureOpenAI` client
   - Requires endpoint, API key, deployment name
   - Same interface as OpenAI

### Provider Selection

```python
def create_llm_provider(settings: Settings) -> ILLMProvider:
    if settings.LLM_PROVIDER == "openai":
        return OpenAIProvider(settings)
    elif settings.LLM_PROVIDER == "azure":
        return AzureOpenAIProvider(settings)
    else:
        raise ValueError(f"Unknown provider: {settings.LLM_PROVIDER}")
```

## Testing Architecture

### Test Layers

1. **Unit Tests** (`tests/unit/`)
   - Test individual entities and services
   - Use mocks for dependencies
   - Fast execution

2. **Integration Tests** (`tests/integration/`)
   - Test complete workflows
   - Use in-memory SQLite database
   - Verify API contracts

3. **Property-Based Tests** (`tests/properties/`)
   - Use Hypothesis for generative testing
   - Verify invariants across many inputs
   - Catch edge cases

### Test Database

- Uses SQLite in-memory for speed
- Automatically created and destroyed per test
- No external dependencies required

## Deployment Architecture

### Docker Compose

```yaml
services:
  db:
    image: postgres:16-alpine
    volumes: [postgres_data]
    healthcheck: pg_isready
  
  backend:
    build: ./backend
    depends_on: [db]
    ports: [8000]
    environment: [DATABASE_URL, API_KEYS, ...]
  
  frontend:
    build: ./frontend
    depends_on: [backend]
    ports: [3000]
    environment: [VITE_API_URL]
```

### Service Communication

```
Frontend (port 3000)
    ↓ HTTP/REST
Backend (port 8000)
    ↓ asyncpg
PostgreSQL (port 5432)
    
Backend
    ↓ HTTPS
OpenAI/Azure OpenAI API
```

## Scalability Considerations

1. **Async/Await**: All I/O operations are non-blocking
2. **Connection Pooling**: Database connections are pooled
3. **Stateless Backend**: Can run multiple instances
4. **Load Balancing**: Frontend can be served from CDN
5. **Caching**: Future: Redis for session/memory caching
6. **Rate Limiting**: Future: Implement per-user rate limits

## Security Considerations

1. **Password Hashing**: bcrypt with salt
2. **JWT Tokens**: Signed with SECRET_KEY, expiring
3. **CORS**: Configured for frontend origin
4. **Input Validation**: Pydantic schemas validate all inputs
5. **SQL Injection**: SQLAlchemy parameterized queries
6. **HTTPS**: Required in production
7. **Environment Variables**: Sensitive data in .env files

## Future Enhancements

1. **RAG Module**: Document storage and semantic search
2. **Tools Module**: Safe execution of user-defined tasks
3. **Advanced Memory**: Semantic categorization and search
4. **Analytics**: Usage tracking and performance monitoring
5. **Multi-language**: Support for multiple languages
6. **Mobile App**: Native mobile applications
7. **Real-time**: WebSocket support for live updates
