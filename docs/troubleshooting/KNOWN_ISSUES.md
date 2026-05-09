# Known Issues & Limitations

**Last Updated**: May 9, 2026  
**Version**: 1.0.0

---

## Current Limitations

### 1. Mock LLM Provider Active

**Status**: ⚠️ Limitation  
**Impact**: Medium

**Description**:
The system is currently using a mock LLM provider instead of the real OpenAI API.

**Reason**:
- OpenAI API key has no credits ($0.00 balance)
- Error: "insufficient_quota"

**Workaround**:
Mock provider returns predefined responses:
- "hello" → English greeting
- "hola" → Spanish greeting
- Other → Generic response

**Resolution**:
Add credits to OpenAI account and update API key in `.env`

**Documentation**: [OpenAI Setup](../configuration/OPENAI_SETUP.md)

---

### 2. No API Rate Limiting

**Status**: ⚠️ Missing Feature  
**Impact**: Medium

**Description**:
The API has no rate limiting implemented. Users can make unlimited requests.

**Risk**:
- Potential abuse
- Resource exhaustion
- High OpenAI costs (when using real API)

**Workaround**:
None currently

**Planned Fix**:
Implement rate limiting using slowapi or similar:
```python
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@router.post("/messages")
@limiter.limit("10/minute")
async def send_message(...):
    ...
```

---

### 3. No Response Caching

**Status**: ⚠️ Missing Feature  
**Impact**: Low

**Description**:
Identical queries result in new API calls, increasing costs and latency.

**Impact**:
- Higher OpenAI costs
- Slower response times for repeated queries

**Workaround**:
None currently

**Planned Fix**:
Implement Redis caching for common queries

---

### 4. Single Instance Only

**Status**: ⚠️ Limitation  
**Impact**: Low (for current scale)

**Description**:
System not configured for horizontal scaling (multiple instances).

**Limitations**:
- No load balancing
- No session sharing
- Single point of failure

**Workaround**:
Sufficient for small-medium scale deployments

**Planned Fix**:
- Add Redis for session storage
- Configure load balancer
- Implement health checks

---

### 5. No Streaming Responses

**Status**: ⚠️ Missing Feature  
**Impact**: Low

**Description**:
Messages are returned only after complete generation, not streamed in real-time.

**Impact**:
- Perceived slower response time
- No progress indication for long responses

**Workaround**:
None currently

**Planned Fix**:
Implement Server-Sent Events (SSE) for streaming:
```python
@router.post("/messages/stream")
async def stream_message(...):
    async for chunk in llm_provider.stream_completion(...):
        yield chunk
```

---

## Browser Compatibility

### Tested Browsers

| Browser | Version | Status |
|---------|---------|--------|
| Chrome | 120+ | ✅ Fully Supported |
| Firefox | 120+ | ✅ Fully Supported |
| Safari | 17+ | ✅ Fully Supported |
| Edge | 120+ | ✅ Fully Supported |

### Known Issues

**Safari < 17**:
- Fetch API may have issues with CORS
- Workaround: Upgrade to Safari 17+

**IE 11**:
- Not supported (uses modern JavaScript features)
- Workaround: Use a modern browser

---

## Performance Considerations

### Database

**Issue**: No connection pooling optimization  
**Impact**: May affect performance under high load  
**Workaround**: Default pool size (5) sufficient for small-medium scale  
**Fix**: Adjust `pool_size` and `max_overflow` in database configuration

### Memory

**Issue**: No memory cleanup for old conversations  
**Impact**: Database grows indefinitely  
**Workaround**: Manual cleanup if needed  
**Fix**: Implement automatic archival/deletion of old conversations

---

## Security Considerations

### 1. No HTTPS in Development

**Status**: ⚠️ Expected (Development)  
**Impact**: High (Production)

**Description**:
Development environment uses HTTP, not HTTPS.

**Risk**:
- Credentials transmitted in plain text
- Vulnerable to man-in-the-middle attacks

**Resolution**:
**Required for production**: Configure SSL/TLS certificate

---

### 2. Default SECRET_KEY

**Status**: ⚠️ Must Change for Production  
**Impact**: Critical

**Description**:
`.env` file contains default SECRET_KEY.

**Risk**:
- JWT tokens can be forged
- Session hijacking possible

**Resolution**:
Generate secure random key for production:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

### 3. No API Key Rotation

**Status**: ⚠️ Missing Feature  
**Impact**: Medium

**Description**:
No automatic rotation of OpenAI API keys.

**Risk**:
- Compromised keys remain valid indefinitely

**Resolution**:
Manually rotate keys every 90 days

---

## Deployment Limitations

### Docker Compose

**Limitation**: Not suitable for large-scale production  
**Reason**: Single-host deployment, no orchestration  
**Recommendation**: Use Kubernetes for production scale

### Environment Variables

**Limitation**: Vite env vars baked at build time  
**Impact**: Frontend requires rebuild for env changes  
**Workaround**: Use runtime configuration for production

---

## OpenAI API Limitations

### Rate Limits

**Free Tier**:
- 3 requests per minute
- 200 requests per day

**Paid Tier**:
- 3,500 requests per minute (GPT-3.5)
- 10,000 requests per minute (GPT-4)

**Workaround**: Use mock provider for development

### Model Access

**Issue**: Not all accounts have access to all models  
**Impact**: GPT-4 may not be available  
**Workaround**: Use gpt-3.5-turbo (widely available)

### Costs

**Issue**: API calls cost money  
**Impact**: Unexpected charges possible  
**Mitigation**: Set spending limits in OpenAI dashboard

---

## Workarounds Summary

| Issue | Workaround | Permanent Fix |
|-------|------------|---------------|
| No OpenAI credits | Use mock provider | Add credits |
| No rate limiting | Monitor usage | Implement slowapi |
| No caching | Accept higher costs | Add Redis |
| No streaming | Wait for full response | Implement SSE |
| HTTP only | OK for development | Add HTTPS |
| Default SECRET_KEY | OK for development | Generate secure key |

---

## Reporting Issues

### How to Report

1. **Check this document** - Issue may be known
2. **Check troubleshooting** - [Troubleshooting Guide](./TROUBLESHOOTING.md)
3. **Search GitHub Issues** - May already be reported
4. **Create new issue** - Provide details:
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Environment (OS, Docker version, etc.)
   - Logs (if applicable)

### Issue Template

```markdown
**Description**: Brief description of the issue

**Steps to Reproduce**:
1. Step 1
2. Step 2
3. Step 3

**Expected Behavior**: What should happen

**Actual Behavior**: What actually happens

**Environment**:
- OS: macOS/Linux/Windows
- Docker: version
- Browser: Chrome 120

**Logs**:
```
Paste relevant logs here
```
```

---

## Planned Improvements

### Short Term (Next Release)

1. ✅ Add rate limiting
2. ✅ Implement response caching
3. ✅ Add streaming responses
4. ✅ Improve error messages

### Medium Term

1. ✅ Horizontal scaling support
2. ✅ Redis integration
3. ✅ Monitoring dashboard
4. ✅ Automated backups

### Long Term

1. ✅ Multi-language support
2. ✅ Voice input/output
3. ✅ Mobile app
4. ✅ Plugin system

---

## Related Documentation

- [Troubleshooting Guide](./TROUBLESHOOTING.md) - Fix common issues
- [OpenAI Setup](../configuration/OPENAI_SETUP.md) - Configure API
- [Bug Fixes](../releases/BUG_FIXES.md) - Fixed issues

---

**Status**: ✅ All Known Issues Documented  
**Next Review**: Next release
