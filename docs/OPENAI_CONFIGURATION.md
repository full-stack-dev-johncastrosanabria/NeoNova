# OpenAI Configuration Guide

**Date**: May 9, 2026  
**Status**: ✅ Configured

---

## Configuration Status

✅ **OpenAI API Key**: Configured  
✅ **LLM Provider**: openai  
✅ **Model**: gpt-4  
✅ **Backend**: Ready to use OpenAI

---

## Environment Variables

The following environment variables are configured in `.env`:

```env
# LLM Provider Configuration
LLM_PROVIDER=openai

# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-4
```

---

## How It Works

### Message Flow

1. **User sends message** → Frontend sends to `/conversations/{id}/messages`
2. **Backend receives message** → Stores in database
3. **LLM Provider called** → OpenAI generates response
4. **Response stored** → Assistant message saved to database
5. **Response returned** → Frontend displays to user

### OpenAI Provider Implementation

**File**: `/backend/src/infrastructure/llm_providers/openai_provider.py`

**Key Features**:
- Reuses single HTTP client for efficiency
- Handles rate limiting errors gracefully
- Returns structured LLM responses with usage metadata
- Supports both chat completions and embeddings

**Error Handling**:
- Rate limit errors → Returns 429 with retry message
- Connection errors → Returns 503 Service Unavailable
- API errors → Returns 503 with error details

---

## Testing the Configuration

### 1. Verify Configuration
```bash
docker-compose exec backend python -c \
  "from application.config import get_settings; \
   s = get_settings(); \
   print(f'OpenAI API Key: {bool(s.OPENAI_API_KEY)}'); \
   print(f'LLM Provider: {s.LLM_PROVIDER}'); \
   print(f'Model: {s.OPENAI_MODEL}')"
```

Expected output:
```
OpenAI API Key: True
LLM Provider: openai
Model: gpt-4
```

### 2. Test Message Endpoint
```bash
# Get token
TOKEN=$(curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"password12"}' \
  | grep -o '"token":"[^"]*' | cut -d'"' -f4)

# Get conversation
CONV_ID=$(curl -s -X GET http://localhost:8000/conversations/ \
  -H "Authorization: Bearer $TOKEN" \
  | grep -o '"id":"[^"]*' | head -1 | cut -d'"' -f4)

# Send message
curl -X POST http://localhost:8000/conversations/$CONV_ID/messages \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"content":"Hello, how are you?"}'
```

### 3. Check Backend Logs
```bash
docker-compose logs backend -f
```

---

## Troubleshooting

### Issue: 503 Service Unavailable

**Possible Causes**:
1. OpenAI API rate limit exceeded
2. Network connectivity issue
3. Invalid API key
4. OpenAI service down

**Solutions**:
1. Wait a few minutes and retry
2. Check internet connection
3. Verify API key in `.env`
4. Check OpenAI status page

### Issue: 401 Unauthorized

**Cause**: Invalid or expired API key

**Solution**: 
1. Get new API key from https://platform.openai.com/api-keys
2. Update `.env` file
3. Restart backend: `docker-compose restart backend`

### Issue: Slow Responses

**Cause**: OpenAI API latency or rate limiting

**Solutions**:
1. Reduce request frequency
2. Use a faster model (e.g., gpt-3.5-turbo)
3. Check OpenAI usage dashboard

---

## API Key Security

### Best Practices

1. **Never commit API keys** to version control
2. **Use environment variables** for sensitive data
3. **Rotate keys regularly** for security
4. **Monitor usage** on OpenAI dashboard
5. **Set spending limits** to prevent unexpected charges

### For Production

1. Use a secrets management system (e.g., AWS Secrets Manager)
2. Implement API key rotation
3. Monitor and log all API calls
4. Set up alerts for unusual activity
5. Use separate keys for development and production

---

## Configuration Options

### Alternative Models

To use a different OpenAI model, update `.env`:

```env
# For faster responses (cheaper)
OPENAI_MODEL=gpt-3.5-turbo

# For better quality
OPENAI_MODEL=gpt-4-turbo

# For latest model
OPENAI_MODEL=gpt-4o
```

### Alternative LLM Providers

To use Azure OpenAI instead:

```env
LLM_PROVIDER=azure_openai
AZURE_OPENAI_API_KEY=your-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment
```

---

## Usage Monitoring

### Check OpenAI Usage

1. Go to https://platform.openai.com/account/usage/overview
2. View API usage and costs
3. Set spending limits if needed

### Monitor in Application

The backend logs all API calls with:
- Request timestamp
- Model used
- Tokens used (prompt + completion)
- Response time

---

## Performance Optimization

### Tips for Better Performance

1. **Use streaming** for long responses (future enhancement)
2. **Cache embeddings** for frequently used content
3. **Batch requests** when possible
4. **Use appropriate model** for task complexity
5. **Implement retry logic** with exponential backoff

### Current Implementation

- ✅ Single HTTP client reuse
- ✅ Proper error handling
- ✅ Usage tracking
- ✅ Rate limit handling
- ⏳ Streaming (future)
- ⏳ Caching (future)

---

## API Reference

### Generate Completion

**Endpoint**: `POST /conversations/{id}/messages`

**Request**:
```json
{
  "content": "Your message here"
}
```

**Response** (Success):
```json
{
  "id": "message-id",
  "conversation_id": "conv-id",
  "role": "assistant",
  "content": "AI response",
  "metadata": {
    "model": "gpt-4",
    "usage": {
      "prompt_tokens": 10,
      "completion_tokens": 20,
      "total_tokens": 30
    }
  }
}
```

**Response** (Error):
```json
{
  "error": "Service Unavailable",
  "message": "AI service temporarily unavailable",
  "details": null,
  "timestamp": "2026-05-09T04:23:01.841801+00:00"
}
```

---

## Summary

✅ **OpenAI is fully configured and ready to use**

The NeoNova AI Assistant can now:
- Generate chat completions using GPT-4
- Handle user messages with AI responses
- Track token usage and costs
- Handle errors gracefully

For more information, see:
- `/docs/API.md` - Full API reference
- `/docs/TROUBLESHOOTING.md` - Common issues
- `/docs/ARCHITECTURE.md` - System design

---

**Status**: ✅ **CONFIGURED AND READY**  
**Last Updated**: May 9, 2026  
**API Key**: Configured  
**Model**: gpt-4

