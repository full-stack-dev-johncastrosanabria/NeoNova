# OpenAI Rate Limit Issue - May 9, 2026

## Problem

The chat endpoint is returning **429 Too Many Requests** when sending messages.

### Error Details

```
Status Code: 429 Too Many Requests
Request URL: http://localhost:8000/conversations/{id}/messages
Request Method: POST
```

### Root Cause

The OpenAI API key has hit its rate limit. This happens when:
- Too many requests in a short period
- API key has limited quota
- Free tier limits exceeded

## Solutions

### Option 1: Wait and Retry ⏰

**Recommended for production use**

The rate limit will reset after a period of time (usually a few minutes to an hour depending on your OpenAI plan).

**Steps**:
1. Wait 5-10 minutes
2. Try sending a message again
3. If still rate limited, wait longer

**Check your OpenAI usage**:
- Go to https://platform.openai.com/account/usage
- View current usage and limits
- Check when the rate limit will reset

### Option 2: Use Mock Provider 🎭

**Recommended for testing and development**

Switch to the mock LLM provider that doesn't make real API calls.

**Steps**:

1. **Update `.env` file**:
   ```env
   # Change the API key to a placeholder
   OPENAI_API_KEY=sk-your-openai-api-key-here
   ```

2. **Restart backend**:
   ```bash
   docker-compose restart backend
   ```

3. **Test the chat**:
   - Send a message like "Hello" or "Hola"
   - You'll get a mock response
   - No API calls, no rate limits

**Mock Provider Responses**:
- "hola" → Spanish greeting
- "hello" → English greeting
- "hi" → Friendly greeting
- Other → Generic mock response

### Option 3: Upgrade OpenAI Plan 💳

**For production use with high volume**

Upgrade your OpenAI account to increase rate limits:

1. Go to https://platform.openai.com/account/billing
2. Add payment method
3. Upgrade to a paid plan
4. Higher rate limits and quotas

**Plans**:
- **Free**: Limited requests per minute
- **Pay-as-you-go**: Higher limits, pay per token
- **Enterprise**: Custom limits

### Option 4: Implement Rate Limiting 🚦

**Prevent hitting limits in the first place**

Add rate limiting to your application:

1. **Backend rate limiting**:
   ```python
   from slowapi import Limiter
   from slowapi.util import get_remote_address
   
   limiter = Limiter(key_func=get_remote_address)
   
   @router.post("/messages")
   @limiter.limit("5/minute")  # 5 requests per minute
   async def send_message(...):
       ...
   ```

2. **Frontend debouncing**:
   ```typescript
   // Prevent rapid-fire requests
   const debouncedSendMessage = debounce(sendMessage, 1000);
   ```

3. **Queue system**:
   - Implement a message queue
   - Process messages at a controlled rate
   - Retry failed requests with exponential backoff

## Current Configuration

### Backend

**File**: `/.env`

```env
# Using mock provider (no rate limits)
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-3.5-turbo
```

### Provider Selection

**File**: `/backend/src/infrastructure/llm_providers/factory.py`

The factory automatically detects placeholder API keys:

```python
# If API key starts with "sk-your-", use mock provider
if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY.startswith("sk-your-"):
    return MockLLMProvider(model="mock-gpt-4")

# Otherwise, use real OpenAI provider
return OpenAIProvider(
    api_key=settings.OPENAI_API_KEY,
    model=settings.OPENAI_MODEL,
)
```

## Error Handling

The backend properly handles rate limit errors:

**File**: `/backend/src/infrastructure/llm_providers/openai_provider.py`

```python
try:
    response = await client.chat.completions.create(...)
except openai.RateLimitError as exc:
    raise RateLimitError("Rate limit exceeded, please try again later") from exc
```

**File**: `/backend/src/main.py`

```python
@app.exception_handler(RateLimitError)
async def rate_limit_error_handler(request: Request, exc: RateLimitError):
    return JSONResponse(
        status_code=429,
        content={
            "error": "Too Many Requests",
            "message": str(exc) or "Rate limit exceeded. Please try again later.",
            "details": None,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )
```

## Testing

### Test with Mock Provider

```bash
# 1. Ensure mock provider is active
docker-compose exec backend python -c \
  "from application.config import get_settings; \
   s = get_settings(); \
   print(f'API Key: {s.OPENAI_API_KEY[:20]}...')"

# Should show: API Key: sk-your-openai-api-k...

# 2. Send a test message
curl -X POST http://localhost:8000/conversations/{id}/messages \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {token}" \
  -d '{"content":"Hello"}'

# Should return mock response immediately
```

### Test with Real API (After Rate Limit Reset)

```bash
# 1. Update .env with real API key
OPENAI_API_KEY=sk-proj-your-real-key-here

# 2. Restart backend
docker-compose restart backend

# 3. Send a test message
# Should return real GPT-3.5-turbo response
```

## Monitoring

### Check OpenAI Usage

```bash
# View usage dashboard
open https://platform.openai.com/account/usage
```

### Check Backend Logs

```bash
# Watch for rate limit errors
docker-compose logs backend -f | grep -i "429\|rate"
```

### Check Current Provider

```bash
# See which provider is active
docker-compose exec backend python -c \
  "from infrastructure.llm_providers.factory import create_llm_provider; \
   from application.config import get_settings; \
   provider = create_llm_provider(get_settings()); \
   print(f'Provider: {type(provider).__name__}')"
```

## Prevention Tips

1. **Monitor usage** regularly on OpenAI dashboard
2. **Set spending limits** to prevent unexpected charges
3. **Implement caching** for common queries
4. **Use mock provider** for development and testing
5. **Add rate limiting** to your application
6. **Implement retry logic** with exponential backoff
7. **Queue messages** during high traffic

## Summary

✅ **Issue**: 429 Too Many Requests from OpenAI API  
✅ **Cause**: Rate limit exceeded  
✅ **Solution**: Switched to mock provider for testing  
✅ **Status**: **RESOLVED**

### Current Setup

- **Provider**: Mock LLM Provider
- **Rate Limits**: None (mock provider)
- **API Calls**: None (no external requests)
- **Responses**: Simulated responses

### To Switch Back to Real API

1. Get a new API key or wait for rate limit reset
2. Update `.env` with real key
3. Restart backend: `docker-compose restart backend`

---

**Date**: May 9, 2026  
**Status**: ✅ **USING MOCK PROVIDER**  
**Next Steps**: Wait for rate limit reset or upgrade OpenAI plan
