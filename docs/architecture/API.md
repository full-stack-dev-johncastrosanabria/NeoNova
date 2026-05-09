# NeoNova API Documentation

## Base URL

```
http://localhost:8000
```

## Authentication

All protected endpoints require a Bearer token in the Authorization header:

```
Authorization: Bearer <token>
```

## Response Format

### Success Response

```json
{
  "id": "uuid",
  "field": "value",
  "created_at": "2024-05-08T12:00:00Z"
}
```

### Error Response

```json
{
  "error": "Error Type",
  "message": "Descriptive error message",
  "details": null,
  "timestamp": "2024-05-08T12:00:00Z"
}
```

## Endpoints

### Authentication

#### Register User

```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123",
  "display_name": "John Doe"
}
```

**Response**: `201 Created`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "display_name": "John Doe",
  "created_at": "2024-05-08T12:00:00Z"
}
```

**Errors**:
- `400`: Email already registered
- `422`: Validation error (invalid email, password < 8 chars)

#### Login

```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response**: `200 OK`
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "display_name": "John Doe",
    "created_at": "2024-05-08T12:00:00Z"
  }
}
```

**Errors**:
- `401`: Invalid credentials

---

### Conversations

#### Create Conversation

```http
POST /conversations/
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "My First Conversation"
}
```

**Response**: `201 Created`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "My First Conversation",
  "created_at": "2024-05-08T12:00:00Z",
  "updated_at": "2024-05-08T12:00:00Z"
}
```

**Errors**:
- `400`: Empty title
- `401`: Unauthorized

#### List Conversations

```http
GET /conversations/
Authorization: Bearer <token>
```

**Response**: `200 OK`
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "My First Conversation",
    "created_at": "2024-05-08T12:00:00Z",
    "updated_at": "2024-05-08T12:00:00Z"
  }
]
```

#### Delete Conversation

```http
DELETE /conversations/{conversation_id}
Authorization: Bearer <token>
```

**Response**: `204 No Content`

**Errors**:
- `404`: Conversation not found
- `401`: Unauthorized

---

### Messages

#### Send Message

```http
POST /conversations/{conversation_id}/messages
Authorization: Bearer <token>
Content-Type: application/json

{
  "content": "Hello, what can you help me with?"
}
```

**Response**: `200 OK`
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440002",
    "conversation_id": "550e8400-e29b-41d4-a716-446655440001",
    "role": "user",
    "content": "Hello, what can you help me with?",
    "metadata_json": null,
    "created_at": "2024-05-08T12:00:00Z"
  },
  {
    "id": "550e8400-e29b-41d4-a716-446655440003",
    "conversation_id": "550e8400-e29b-41d4-a716-446655440001",
    "role": "assistant",
    "content": "I can help you with...",
    "metadata_json": {
      "model": "gpt-4o-mini",
      "usage": {
        "prompt_tokens": 10,
        "completion_tokens": 20,
        "total_tokens": 30
      }
    },
    "created_at": "2024-05-08T12:00:01Z"
  }
]
```

**Errors**:
- `400`: Empty message
- `404`: Conversation not found
- `401`: Unauthorized

#### List Messages

```http
GET /conversations/{conversation_id}/messages
Authorization: Bearer <token>
```

**Response**: `200 OK`
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440002",
    "conversation_id": "550e8400-e29b-41d4-a716-446655440001",
    "role": "user",
    "content": "Hello, what can you help me with?",
    "metadata_json": null,
    "created_at": "2024-05-08T12:00:00Z"
  },
  {
    "id": "550e8400-e29b-41d4-a716-446655440003",
    "conversation_id": "550e8400-e29b-41d4-a716-446655440001",
    "role": "assistant",
    "content": "I can help you with...",
    "metadata_json": {...},
    "created_at": "2024-05-08T12:00:01Z"
  }
]
```

---

### Memories

#### List Memories

```http
GET /memories/
Authorization: Bearer <token>
```

**Response**: `200 OK`
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440004",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "type": "preference",
    "content": "I prefer concise responses",
    "importance": 3,
    "source_message_id": null,
    "is_active": true,
    "created_at": "2024-05-08T12:00:00Z",
    "updated_at": "2024-05-08T12:00:00Z"
  }
]
```

#### Create Memory

```http
POST /memories/
Authorization: Bearer <token>
Content-Type: application/json

{
  "type": "preference",
  "content": "I prefer concise responses",
  "importance": 3
}
```

**Response**: `201 Created`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440004",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "type": "preference",
  "content": "I prefer concise responses",
  "importance": 3,
  "source_message_id": null,
  "is_active": true,
  "created_at": "2024-05-08T12:00:00Z",
  "updated_at": "2024-05-08T12:00:00Z"
}
```

**Memory Types**:
- `preference`: User preferences
- `fact`: Facts about the user
- `instruction`: Instructions for the assistant
- `correction`: Corrections from user feedback
- `project_context`: Project-specific context

**Importance Levels**:
- `1`: Low
- `2`: Medium
- `3`: High
- `4`: Critical

#### Deactivate Memory

```http
DELETE /memories/{memory_id}
Authorization: Bearer <token>
```

**Response**: `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440004",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "type": "preference",
  "content": "I prefer concise responses",
  "importance": 3,
  "source_message_id": null,
  "is_active": false,
  "created_at": "2024-05-08T12:00:00Z",
  "updated_at": "2024-05-08T12:00:01Z"
}
```

---

### Feedback

#### Create Feedback

```http
POST /feedback/
Authorization: Bearer <token>
Content-Type: application/json

{
  "message_id": "550e8400-e29b-41d4-a716-446655440003",
  "rating": 4,
  "comment": "Good response, but could be more detailed",
  "correction": "Actually, the correct approach is..."
}
```

**Response**: `201 Created`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440005",
  "message_id": "550e8400-e29b-41d4-a716-446655440003",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "rating": 4,
  "comment": "Good response, but could be more detailed",
  "correction": "Actually, the correct approach is...",
  "created_at": "2024-05-08T12:00:00Z"
}
```

**Notes**:
- If `correction` is provided, a Memory with type=`correction` and importance=`3` (HIGH) is automatically created
- Only one feedback per message is allowed

**Errors**:
- `404`: Message not found
- `409`: Feedback already exists for this message
- `401`: Unauthorized

---

### Health Check

#### Check API Health

```http
GET /health
```

**Response**: `200 OK`
```json
{
  "status": "ok"
}
```

---

## HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request succeeded |
| 201 | Created - Resource created |
| 204 | No Content - Request succeeded, no response body |
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Missing or invalid token |
| 404 | Not Found - Resource not found |
| 409 | Conflict - Resource already exists |
| 422 | Unprocessable Entity - Validation error |
| 500 | Internal Server Error - Server error |
| 503 | Service Unavailable - LLM provider unavailable |

---

## Rate Limiting

Currently not implemented. Future versions will include:
- Per-user rate limits
- Per-endpoint rate limits
- Exponential backoff for LLM provider errors

---

## Pagination

Currently not implemented. Future versions will include:
- Limit/offset pagination for list endpoints
- Cursor-based pagination for large datasets

---

## WebSocket Support

Currently not implemented. Future versions will include:
- Real-time message streaming
- Live conversation updates
- Typing indicators

---

## API Documentation

### Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### OpenAPI Schema

```http
GET /openapi.json
```

---

## Examples

### Complete Conversation Flow

```bash
# 1. Register
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123",
    "display_name": "John Doe"
  }'

# 2. Login
TOKEN=$(curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }' | jq -r '.token')

# 3. Create conversation
CONV_ID=$(curl -X POST http://localhost:8000/conversations/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "My Chat"}' | jq -r '.id')

# 4. Send message
curl -X POST http://localhost:8000/conversations/$CONV_ID/messages \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content": "Hello!"}'

# 5. Create memory
curl -X POST http://localhost:8000/memories/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "preference",
    "content": "I like concise responses",
    "importance": 3
  }'
```

---

## Troubleshooting

### 401 Unauthorized

- Token is missing or invalid
- Token has expired
- User account was deleted

**Solution**: Login again to get a new token

### 404 Not Found

- Resource doesn't exist
- Resource belongs to another user
- Conversation/message was deleted

**Solution**: Verify the resource ID and ownership

### 422 Unprocessable Entity

- Invalid input format
- Missing required fields
- Invalid field values

**Solution**: Check request body against schema

### 503 Service Unavailable

- LLM provider is down
- Rate limit exceeded
- Network connectivity issue

**Solution**: Retry after a delay or check provider status
