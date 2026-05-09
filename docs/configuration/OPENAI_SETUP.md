# OpenAI Configuration Guide

**Last Updated**: May 9, 2026  
**Status**: ✅ Configured with Mock Provider

---

## Overview

NeoNova supports multiple LLM providers. This guide covers OpenAI API integration, including setup, troubleshooting, and the mock provider fallback.

---

## Quick Start

### Option 1: Mock Provider (No API Key Required)

**Best for**: Development, testing, demos

```env
# .env file
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-3.5-turbo
LLM_PROVIDER=openai
```

**Features**:
- ✅ No API costs
- ✅ Instant responses
- ✅ No rate limits
- ✅ Predefined responses for common inputs

**Mock Responses**:
- "hello" → English greeting
- "hola" → Spanish greeting  
- "hi" → Friendly greeting
- Other → Generic response with input preview

### Option 2: Real OpenAI API

**Best for**: Production, real AI responses

1. **Get API Key**:
   - Go to https://platform.openai.com/api-keys
   - Create new secret key
   - Copy the key (starts with `sk-proj-` or `sk-`)

2. **Add Credits**:
   - Go to https://platform.openai.com/account/billing
   - Add payment method
   - Purchase credits (minimum $5)

3. **Configure**:
   ```env
   # .env file
   OPENAI_API_KEY=sk-proj-your-actual-key-here
   OPENAI_MODEL=gpt-3.5-turbo
   LLM_PROVIDER=openai
   ```

4. **Restart Backend**:
   ```bash
   docker-compose restart backend
   ```

---

## Configuration

### Environment Variables

**File**: `/.env`

```env
# LLM Provider Selection
LLM_PROVIDER=openai  # Options: openai, azure_openai

# OpenAI Configuration
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-3.5-turbo

# Azure OpenAI (Alternative)
AZURE_OPENAI_API_KEY=your-azure-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment
```

### Available Models

| Model | Speed | Quality | Cost | Use Case |
|-------|-------|---------|------|----------|
| gpt-3.5-turbo | ⚡⚡⚡ | ⭐⭐⭐ | $ | General chat, fast responses |
| gpt-4 | ⚡⚡ | ⭐⭐⭐⭐⭐ | $$$ | Complex tasks, high quality |
| gpt-4-turbo | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | $$ | Best balance |
| gpt-4o | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | $$ | Latest model |

### Provider Selection Logic

**File**: `/backend/src/infrastructure/llm_providers/factory.py`

```python
def create_llm_provider(settings) -> ILLMProvider:
    # Detects placeholder API keys
    if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY.startswith("sk-your-"):
        return MockLLMProvider(model="mock-gpt-4")
    
    # Uses real OpenAI provider
    return OpenAIProvider(
        api_key=settings.OPENAI_API_KEY,
        model=settings.OPENAI_MODEL,
    )
```

---

## Testing

### Verify Configuration

```bash
# Check which provider is active
docker-compose exec backend python -c \
  "from infrastructure.llm_providers.factory import create_llm_provider; \
   from application.config import get_settings; \
   provider = create_llm_provider(get_settings()); \
   print(f'Provider: {type(provider).__name__}')"
```

**Expected Output**:
- `Provider: MockLLMProvider` - Using mock provider
- `Provider: OpenAIProvider` - Using real OpenAI API

### Test Chat Endpoint

```bash
# 1. Login
TOKEN=$(curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password"}' \
  | jq -r '.token')

# 2. Get conversation ID
CONV_ID=$(curl -s -X GET http://localhost:8000/conversations/ \
  -H "Authorization: Bearer $TOKEN" | jq -r '.[0].id')

# 3. Send message
curl -X POST http://localhost:8000/conversations/$CONV_ID/messages \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"content":"Hello, how are you?"}' | jq .
```

---

## Troubleshooting

### Issue: "insufficient_quota"

**Error**:
```json
{
  "error": {
    "type": "insufficient_quota",
    "message": "You exceeded your current quota..."
  }
}
```

**Cause**: OpenAI account has no credits

**Solutions**:
1. **Add credits**: https://platform.openai.com/account/billing
2. **Use mock provider**: Set `OPENAI_API_KEY=sk-your-openai-api-key-here`

### Issue: "rate_limit_exceeded"

**Error**: 429 Too Many Requests

**Cause**: Too many API calls in short time

**Solutions**:
1. **Wait**: Rate limits reset after a few minutes
2. **Upgrade plan**: Higher tier = higher limits
3. **Use mock provider**: No rate limits

### Issue: "invalid_api_key"

**Error**: 401 Unauthorized

**Cause**: API key is wrong, expired, or revoked

**Solutions**:
1. **Generate new key**: https://platform.openai.com/api-keys
2. **Check key format**: Should start with `sk-`
3. **Verify in dashboard**: Check key is active

### Issue: "model_not_found"

**Error**: 404 - Model does not exist

**Cause**: API key doesn't have access to specified model

**Solutions**:
1. **Use gpt-3.5-turbo**: Most widely available
2. **Check access**: Some models require special access
3. **Update model**: Change `OPENAI_MODEL` in `.env`

---

## Cost Management

### Pricing (GPT-3.5-Turbo)

- **Input**: $0.50 per 1M tokens (~$0.0005 per 1K tokens)
- **Output**: $1.50 per 1M tokens (~$0.0015 per 1K tokens)

### Example Costs

| Usage | Tokens | Cost |
|-------|--------|------|
| 10 messages | 500 | $0.01 |
| 100 messages | 5,000 | $0.10 |
| 1,000 messages | 50,000 | $1.00 |
| 10,000 messages | 500,000 | $10.00 |

### Cost Optimization

1. **Use mock provider** for development
2. **Implement caching** for common queries
3. **Set spending limits** in OpenAI dashboard
4. **Monitor usage** regularly
5. **Use gpt-3.5-turbo** instead of GPT-4 when possible

---

## Monitoring

### Check OpenAI Usage

```bash
# Open usage dashboard
open https://platform.openai.com/account/usage
```

### Check Backend Logs

```bash
# Watch for API errors
docker-compose logs backend -f | grep -i "openai\|error\|quota"
```

### Check Current Balance

Visit: https://platform.openai.com/account/billing/overview

---

## Advanced Configuration

### Azure OpenAI

```env
LLM_PROVIDER=azure_openai
AZURE_OPENAI_API_KEY=your-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment
AZURE_OPENAI_API_VERSION=2023-05-15
```

### Custom Parameters

Edit `/backend/src/infrastructure/llm_providers/openai_provider.py`:

```python
response = await client.chat.completions.create(
    model=self.model,
    messages=openai_messages,
    temperature=0.7,  # Adjust creativity (0.0-2.0)
    max_tokens=None,  # Limit response length
    top_p=1.0,        # Nucleus sampling
    frequency_penalty=0.0,  # Reduce repetition
    presence_penalty=0.0,   # Encourage new topics
)
```

---

## Security Best Practices

1. **Never commit API keys** to version control
2. **Use environment variables** for sensitive data
3. **Rotate keys regularly** (every 90 days)
4. **Set spending limits** to prevent unexpected charges
5. **Monitor usage** for unusual activity
6. **Use separate keys** for dev/staging/production

---

## Summary

### Current Setup

- **Provider**: Mock LLM Provider
- **API Key**: Placeholder (no real API calls)
- **Model**: mock-gpt-4
- **Cost**: $0.00
- **Rate Limits**: None

### To Switch to Real API

1. Get API key from OpenAI
2. Add credits to account ($5 minimum)
3. Update `.env` with real key
4. Restart backend: `docker-compose restart backend`

---

## Related Documentation

- [Architecture](../architecture/ARCHITECTURE.md) - System design
- [API Reference](../architecture/API.md) - REST endpoints
- [Troubleshooting](../troubleshooting/TROUBLESHOOTING.md) - Common issues

---

**Status**: ✅ Configured and Working  
**Provider**: Mock (Development Mode)  
**Next Steps**: Add OpenAI credits for production use
