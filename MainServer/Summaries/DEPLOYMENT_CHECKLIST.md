# 🚀 Railway Deployment Checklist

## ⚠️ Database Connection Issue

The database URL you provided failed authentication. Please follow these steps:

### Step 1: Get Correct Database URL

1. Go to your Railway dashboard
2. Click on your PostgreSQL service
3. Go to the **Variables** tab
4. Look for `DATABASE_URL` or copy these individual values:
   ```
   PGHOST=interchange.proxy.rlwy.net
   PGPORT=23006
   PGDATABASE=easy-download-db
   PGUSER=easy-download
   PGPASSWORD=<COPY_THE_CORRECT_PASSWORD>
   ```

### Step 2: Test Connection Locally

```bash
# Test the database connection
python test_db_connection.py "postgresql://user:password@host:port/database"
```

If successful, proceed to Step 3.

---

## 📋 Pre-Deployment Checklist

### Files Ready ✅
- [x] `app.py` - Main Flask application
- [x] `requirements.txt` - All dependencies
- [x] `Procfile` - Gunicorn configuration
- [x] `runtime.txt` - Python version
- [x] `railway.json` - Railway configuration
- [x] `init_db.py` - Database initialization
- [x] `.env.production` - Production environment variables
- [x] `.gitignore` - Git ignore rules

### Database Models ✅
- [x] User model with IP tracking
- [x] UserActivity model for download history
- [x] Download, Batch, Playlist models
- [x] All relationships configured

### API Endpoints ✅
- [x] Authentication (register, login, profile, activity)
- [x] YouTube single link downloads
- [x] YouTube multi-link batch downloads
- [x] YouTube playlist downloads
- [x] Health checks

---

## 🚀 Deployment Steps

### Option 1: Railway CLI (Recommended)

```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login
railway login

# 3. Navigate to MainServer
cd "d:\Project\Youtube downloader\MainServer"

# 4. Create new project or link existing
railway init
# or
railway link

# 5. Add PostgreSQL service (if not already added)
railway add

# 6. Set environment variables
railway variables set SECRET_KEY="$(openssl rand -hex 32)"
railway variables set JWT_SECRET_KEY="$(openssl rand -hex 32)"
railway variables set FLASK_ENV="production"

# 7. Deploy
railway up

# 8. Check logs
railway logs

# 9. Get deployment URL
railway open
```

### Option 2: GitHub Integration

```bash
# 1. Initialize git repository
cd "d:\Project\Youtube downloader\MainServer"
git init
git add .
git commit -m "Initial deployment - YouTube Downloader API"

# 2. Create GitHub repository
# Go to github.com and create a new repository

# 3. Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main

# 4. Connect to Railway
# - Go to railway.app
# - Click "New Project"
# - Select "Deploy from GitHub repo"
# - Choose your repository
# - Railway will auto-deploy
```

---

## ⚙️ Environment Variables Setup

### Required Variables

Set these in Railway dashboard (Variables tab):

```bash
# Security
SECRET_KEY=<generate-random-32-char-string>
JWT_SECRET_KEY=<generate-random-32-char-string>

# Flask
FLASK_ENV=production
PORT=5000

# Database (automatically set by Railway if PostgreSQL is linked)
DATABASE_URL=${{Postgres.DATABASE_URL}}

# YouTube Downloads
YOUTUBE_TEMP_DIR=./temp
MAX_FILE_SIZE=524288000
MAX_CONCURRENT_DOWNLOADS=3
DOWNLOAD_TIMEOUT=300

# CORS
CORS_ORIGINS=*
```

### Generate Secure Keys

```bash
# On Windows PowerShell
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | % {[char]$_})

# On Linux/Mac
openssl rand -hex 32
```

---

## 🔍 Verification Steps

### 1. Check Deployment Logs

```bash
railway logs
```

Look for:
```
✅ Database tables created successfully!
[INFO] Booting worker with pid: ...
[INFO] Listening at: http://0.0.0.0:5000
```

### 2. Test Health Endpoint

```bash
curl https://your-app.railway.app/health
```

Expected response:
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

### 3. Test Database Connection

```bash
curl https://your-app.railway.app/api/database/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "database-server",
  "database": "postgresql",
  "connected": true
}
```

### 4. Test User Registration

```bash
curl -X POST https://your-app.railway.app/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "confirm_email": "test@example.com",
    "password": "TestPass123!",
    "confirm_password": "TestPass123!"
  }'
```

### 5. Test Login

```bash
curl -X POST https://your-app.railway.app/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "login": "testuser",
    "password": "TestPass123!"
  }'
```

---

## 🐛 Common Issues & Solutions

### Issue 1: Database Connection Failed

**Error**: `password authentication failed`

**Solution**:
1. Go to Railway PostgreSQL service
2. Copy the correct `DATABASE_URL`
3. Update environment variable
4. Redeploy

### Issue 2: Module Not Found

**Error**: `ModuleNotFoundError: No module named 'X'`

**Solution**:
1. Check `requirements.txt` includes the module
2. Redeploy (Railway will reinstall dependencies)

### Issue 3: Port Binding Error

**Error**: `Address already in use`

**Solution**:
- Ensure `app.py` uses `os.getenv('PORT', 5000)`
- Railway automatically sets the PORT variable

### Issue 4: Tables Not Created

**Error**: `relation "users" does not exist`

**Solution**:
```bash
# Manually initialize database
railway run python init_db.py
```

### Issue 5: CORS Errors

**Error**: `CORS policy: No 'Access-Control-Allow-Origin' header`

**Solution**:
- Set `CORS_ORIGINS` to your frontend URL
- Or use `*` for development

---

## 📊 Database Tables Verification

After deployment, verify tables exist:

```bash
railway run python -c "
from DatabaseServer.config import engine
from sqlalchemy import text
with engine.connect() as conn:
    result = conn.execute(text(\"SELECT table_name FROM information_schema.tables WHERE table_schema='public'\"))
    for row in result:
        print(row[0])
"
```

Expected output:
```
users
user_activities
downloads
batches
batch_items
playlists
playlist_items
```

---

## 🎯 Post-Deployment Tasks

### 1. Update Frontend

Update your frontend API URL:
```javascript
const API_URL = 'https://your-app.railway.app';
```

### 2. Test All Features

- [ ] User registration
- [ ] User login
- [ ] Single video download
- [ ] Batch download
- [ ] Playlist download
- [ ] Activity tracking
- [ ] User profile

### 3. Monitor Performance

- Check Railway metrics dashboard
- Monitor database connections
- Review error logs

### 4. Security Hardening

- [ ] Update SECRET_KEY to strong random value
- [ ] Update JWT_SECRET_KEY to strong random value
- [ ] Set CORS_ORIGINS to specific domain
- [ ] Enable HTTPS only
- [ ] Add rate limiting (future enhancement)

---

## 📈 Scaling Considerations

### Current Configuration

```
Workers: 4
Timeout: 300 seconds
Max Concurrent Downloads: 3
```

### To Scale Up

1. **Increase Workers** (in `Procfile`):
   ```
   web: gunicorn app:app --workers 8 --timeout 300
   ```

2. **Increase Concurrent Downloads**:
   ```bash
   railway variables set MAX_CONCURRENT_DOWNLOADS=5
   ```

3. **Add Redis** (for caching and queues):
   ```bash
   railway add
   # Select Redis
   ```

---

## 🔗 Useful Railway Commands

```bash
# View all services
railway status

# View environment variables
railway variables

# Set a variable
railway variables set KEY=value

# Delete a variable
railway variables delete KEY

# View logs (live)
railway logs --follow

# Open Railway dashboard
railway open

# SSH into container
railway shell

# Run one-off command
railway run python init_db.py
```

---

## ✅ Final Checklist

Before going live:

- [ ] Database connection tested and working
- [ ] All tables created successfully
- [ ] Health endpoints responding
- [ ] User registration working
- [ ] User login working
- [ ] Downloads working
- [ ] Activity tracking working
- [ ] Environment variables set correctly
- [ ] Secrets are strong and random
- [ ] CORS configured properly
- [ ] Frontend updated with API URL
- [ ] All features tested end-to-end

---

## 🎉 Success!

Once all checks pass, your YouTube Downloader API is live on Railway!

**Your API URL**: `https://your-app.railway.app`

**Next Steps**:
1. Share API URL with frontend team
2. Monitor logs for any issues
3. Set up monitoring/alerts
4. Plan for scaling if needed

---

## 📞 Support Resources

- **Railway Docs**: https://docs.railway.app
- **Railway Discord**: https://discord.gg/railway
- **Project Docs**: See `README.md`, `API_DOCUMENTATION.md`, `AUTH_DOCUMENTATION.md`
