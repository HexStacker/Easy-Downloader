# 🔗 Frontend-Backend Integration Guide

## ✅ Configuration Updated

Your backend is now configured to work with your Vercel frontend!

### Frontend URL
```
https://downlode-easy.vercel.app
```

### Backend URL (After Railway Deployment)
```
https://your-app.railway.app
```

---

## 🔧 CORS Configuration

### Updated Settings
- **CORS_ORIGINS**: `https://downlode-easy.vercel.app`
- This allows your Vercel frontend to make API requests to the Railway backend
- Prevents CORS errors in the browser

### Files Updated
- ✅ `.env.example` - CORS updated
- ✅ `.env.production` - CORS updated
- ✅ `RAILWAY_ENV_VARS.md` - Documentation updated

---

## 🚀 Deployment Steps

### Step 1: Deploy Backend to Railway

```bash
# Set environment variables (including CORS)
railway variables set CORS_ORIGINS="https://downlode-easy.vercel.app"

# Deploy
railway up

# Get your Railway URL
railway open
```

Your Railway URL will be something like:
```
https://mainserver-production-xxxx.up.railway.app
```

### Step 2: Update Frontend with Backend URL

In your Vercel frontend project, update the API base URL:

**Example: `src/config/api.js` or similar**
```javascript
// Replace with your actual Railway URL
export const API_BASE_URL = 'https://mainserver-production-xxxx.up.railway.app';

// Or use environment variable
export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';
```

**Vercel Environment Variable:**
1. Go to Vercel Dashboard → Your Project → Settings → Environment Variables
2. Add:
   - Name: `REACT_APP_API_URL` (or `VITE_API_URL` for Vite)
   - Value: `https://your-railway-url.railway.app`
3. Redeploy frontend

---

## 📡 API Endpoints

Once both are deployed, your frontend can call:

### Authentication
```javascript
// Register
POST https://your-railway-url.railway.app/api/auth/register
{
  "username": "user123",
  "email": "user@example.com",
  "confirm_email": "user@example.com",
  "password": "SecurePass123!",
  "confirm_password": "SecurePass123!"
}

// Login
POST https://your-railway-url.railway.app/api/auth/login
{
  "login": "user123",
  "password": "SecurePass123!"
}

// Get Profile (with JWT token)
GET https://your-railway-url.railway.app/api/auth/profile
Headers: { Authorization: "Bearer <token>" }

// Get Activity History
GET https://your-railway-url.railway.app/api/auth/activity?limit=50
Headers: { Authorization: "Bearer <token>" }
```

### YouTube Downloads
```javascript
// Get Video Info
POST https://your-railway-url.railway.app/api/youtube/single/info
{
  "url": "https://youtube.com/watch?v=..."
}

// Download Single Video
POST https://your-railway-url.railway.app/api/youtube/single/download
{
  "url": "https://youtube.com/watch?v=...",
  "format": "mp4",
  "quality": "720p"
}

// Batch Download
POST https://your-railway-url.railway.app/api/youtube/multi/batch
{
  "urls": ["url1", "url2", "url3"],
  "format": "mp4",
  "quality": "best"
}

// Playlist Download
POST https://your-railway-url.railway.app/api/youtube/playlist/download
{
  "url": "https://youtube.com/playlist?list=...",
  "format": "mp4",
  "quality": "1080p"
}
```

---

## 🔐 Authentication Flow

### 1. User Registration
```javascript
const register = async (userData) => {
  const response = await fetch(`${API_BASE_URL}/api/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(userData)
  });
  return await response.json();
};
```

### 2. User Login
```javascript
const login = async (credentials) => {
  const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(credentials)
  });
  const data = await response.json();
  
  // Store JWT token
  localStorage.setItem('token', data.token);
  return data;
};
```

### 3. Authenticated Requests
```javascript
const getProfile = async () => {
  const token = localStorage.getItem('token');
  const response = await fetch(`${API_BASE_URL}/api/auth/profile`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  return await response.json();
};
```

### 4. Download Video
```javascript
const downloadVideo = async (url, format, quality) => {
  const token = localStorage.getItem('token');
  const response = await fetch(`${API_BASE_URL}/api/youtube/single/download`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ url, format, quality })
  });
  return await response.json();
};
```

---

## 🧪 Testing Integration

### 1. Test CORS
```javascript
// From your Vercel frontend console
fetch('https://your-railway-url.railway.app/health')
  .then(r => r.json())
  .then(console.log)
  .catch(console.error);
```

Should return:
```json
{
  "status": "healthy",
  "services": {
    "youtube": "running",
    "auth": "running",
    "database": "running"
  }
}
```

### 2. Test Registration
```javascript
fetch('https://your-railway-url.railway.app/api/auth/register', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    username: 'testuser',
    email: 'test@example.com',
    confirm_email: 'test@example.com',
    password: 'TestPass123!',
    confirm_password: 'TestPass123!'
  })
})
.then(r => r.json())
.then(console.log);
```

---

## 📋 Environment Variables Summary

### Railway (Backend)
```bash
SECRET_KEY=aNTLgMV8rbJGRSomY61UfP4ACQ5kjnspxEHOuB3qtDwlX9KW2ev7iZzy0dcIFh
JWT_SECRET_KEY=UMiTyKwuvn2N7ZjlSBqhXRDxYFJ6csOoLf8tC4bPrHA50mGk9WI3VeQ1padzEg
FLASK_ENV=production
DATABASE_URL=postgresql://postgres:sWzjTuwXcmRwdhpaokPNCPAASjjDfyQS@interchange.proxy.rlwy.net:23006/easy-download-db
CORS_ORIGINS=https://downlode-easy.vercel.app
```

### Vercel (Frontend)
```bash
REACT_APP_API_URL=https://your-railway-url.railway.app
# or for Vite
VITE_API_URL=https://your-railway-url.railway.app
```

---

## 🐛 Troubleshooting

### CORS Error
**Error**: `Access to fetch at '...' from origin 'https://downlode-easy.vercel.app' has been blocked by CORS policy`

**Solution**:
1. Verify `CORS_ORIGINS` is set in Railway:
   ```bash
   railway variables get CORS_ORIGINS
   ```
2. Should return: `https://downlode-easy.vercel.app`
3. If not, set it:
   ```bash
   railway variables set CORS_ORIGINS="https://downlode-easy.vercel.app"
   ```
4. Redeploy: `railway up`

### 401 Unauthorized
**Error**: `401 Unauthorized` on protected endpoints

**Solution**:
1. Ensure JWT token is included in headers
2. Check token is not expired (7-day expiry)
3. Verify token format: `Bearer <token>`

### Network Error
**Error**: `Failed to fetch` or `Network request failed`

**Solution**:
1. Check Railway backend is running: `railway status`
2. Test health endpoint: `curl https://your-railway-url.railway.app/health`
3. Verify frontend has correct API URL

---

## ✅ Integration Checklist

### Backend (Railway)
- [x] Docker configuration ready
- [x] Database created and initialized
- [x] Secure keys generated
- [x] CORS configured for Vercel frontend
- [ ] Deployed to Railway
- [ ] Environment variables set
- [ ] Health endpoint tested

### Frontend (Vercel)
- [ ] API base URL updated with Railway URL
- [ ] Environment variable set in Vercel
- [ ] Authentication flow implemented
- [ ] Download functionality integrated
- [ ] Error handling implemented
- [ ] Redeployed to Vercel

### Testing
- [ ] CORS working (no errors in console)
- [ ] User registration working
- [ ] User login working
- [ ] JWT token stored and used
- [ ] Video download working
- [ ] Activity tracking working

---

## 🎯 Quick Setup Commands

```bash
# Backend (Railway)
cd "d:\Project\Youtube downloader\MainServer"
railway variables set CORS_ORIGINS="https://downlode-easy.vercel.app"
railway up

# Frontend (Vercel)
# Update .env.production or .env
echo "VITE_API_URL=https://your-railway-url.railway.app" > .env.production
git add .
git commit -m "Update API URL"
git push
# Vercel will auto-deploy
```

---

## 📞 Support

If you encounter issues:
1. Check Railway logs: `railway logs`
2. Check Vercel logs in dashboard
3. Test endpoints with curl or Postman
4. Verify CORS settings
5. Check browser console for errors

---

## 🎊 You're Ready!

Your backend is configured to work with your Vercel frontend at:
- **Frontend**: `https://downlode-easy.vercel.app`
- **Backend**: `https://your-railway-url.railway.app` (after deployment)

Just deploy both and they'll work together! 🚀
