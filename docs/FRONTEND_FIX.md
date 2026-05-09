# Frontend Registration Issue Fix - May 9, 2026

## Problem

The frontend registration form was showing a **"Network Error"** when trying to register a new user. The browser's network tab showed:
- **Status**: 400 Bad Request
- **Request**: OPTIONS /auth/register
- **Error**: Network Error displayed to user

## Root Cause

The frontend Docker image was built with an outdated or incorrect API URL configuration. When Vite builds the frontend, it bakes environment variables (like `VITE_API_URL`) into the JavaScript bundle at build time. Changes to the `.env` file after the Docker image is built have no effect.

### Technical Details

1. **Frontend Build Process**:
   - Frontend is built during `docker build` (multi-stage Dockerfile)
   - Vite replaces `import.meta.env.VITE_API_URL` with the actual value at build time
   - The built static files are served by nginx

2. **Environment Variable Timing**:
   - `.env` file is read during `npm run build`
   - Changes to `.env` after build require a rebuild
   - Docker image caches the built files

3. **CORS Configuration**:
   - Backend CORS was configured correctly for `http://localhost:3000`
   - OPTIONS preflight requests were working when tested directly
   - The issue was the frontend making requests to the wrong URL

## Solution

Rebuilt the frontend Docker image to include the correct API URL configuration.

### Steps Taken

1. **Verified `.env` configuration**:
   ```env
   VITE_API_URL=http://localhost:8000
   ```

2. **Rebuilt frontend image**:
   ```bash
   docker-compose build frontend
   ```

3. **Restarted frontend container**:
   ```bash
   docker-compose up -d frontend
   ```

## Files Involved

| File | Purpose |
|------|---------|
| `/frontend/.env` | Environment variables for Vite build |
| `/frontend/Dockerfile` | Multi-stage build (Node + Nginx) |
| `/frontend/src/api/client.ts` | API client using `import.meta.env.VITE_API_URL` |

## Verification

### Test Registration

1. Open browser to `http://localhost:3000`
2. Navigate to registration page
3. Fill in form:
   - Display Name: `qwerty`
   - Email: `qwerty@example.com`
   - Password: `********`
4. Click "Create Account"
5. Should receive success response (201 Created)

### Check Backend Logs

```bash
docker-compose logs backend --tail=20
```

Should show:
```
INFO: 172.66.0.243:xxxxx - "POST /auth/register HTTP/1.1" 201 Created
```

## Prevention

### For Development

When changing environment variables in `/frontend/.env`:

1. **Rebuild the frontend**:
   ```bash
   docker-compose build frontend
   docker-compose up -d frontend
   ```

2. **Or use docker-compose override** for development:
   ```yaml
   # docker-compose.override.yml
   services:
     frontend:
       environment:
         - VITE_API_URL=http://localhost:8000
   ```

### For Production

1. **Use build arguments**:
   ```dockerfile
   ARG VITE_API_URL
   ENV VITE_API_URL=$VITE_API_URL
   ```

2. **Pass at build time**:
   ```bash
   docker build --build-arg VITE_API_URL=https://api.example.com -t frontend .
   ```

## Related Issues

### CORS Configuration

The backend CORS is configured in `/backend/src/main.py`:

```python
raw_origins = os.getenv("CORS_ALLOW_ORIGINS", "http://localhost:5173")
allow_origins = [o.strip() for o in raw_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Current configuration (from docker-compose.yml):
```yaml
CORS_ALLOW_ORIGINS: http://localhost:3000,http://frontend:3000
```

This allows requests from:
- `http://localhost:3000` (browser → backend)
- `http://frontend:3000` (container → container)

## Testing

### Manual Test

```bash
# Test OPTIONS preflight
curl -X OPTIONS http://localhost:8000/auth/register \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: content-type" \
  -v

# Should return 200 OK with CORS headers

# Test POST registration
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -H "Origin: http://localhost:3000" \
  -d '{"email":"test@example.com","password":"password123","display_name":"Test User"}'

# Should return 201 Created
```

## Summary

✅ **Issue**: Frontend showing "Network Error" on registration  
✅ **Cause**: Frontend built with incorrect API URL  
✅ **Fix**: Rebuilt frontend Docker image  
✅ **Status**: **RESOLVED**

### Key Takeaways

1. **Vite environment variables** are baked in at build time
2. **Docker images** cache built files
3. **Changes to `.env`** require rebuild for Docker deployments
4. **CORS configuration** was correct all along

---

**Date**: May 9, 2026  
**Status**: ✅ **FIXED**  
**Commit**: Pending
