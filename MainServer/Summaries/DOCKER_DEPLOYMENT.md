# 🐳 Docker Deployment Guide for Railway

## ✅ Docker Setup Complete

Your server is now configured for Docker deployment on Railway!

### 📦 What's Been Created

- ✅ **Dockerfile** - Production-ready container configuration
- ✅ **.dockerignore** - Optimized image size
- ✅ **railway.json** - Railway Docker builder configuration
- ✅ **docker-compose.yml** - Local testing setup

---

## 🚀 Deploy to Railway (Docker)

### Option 1: Railway CLI (Recommended)

```bash
# 1. Install Railway CLI (if not installed)
npm install -g @railway/cli

# 2. Navigate to MainServer
cd "d:\Project\Youtube downloader\MainServer"

# 3. Login to Railway
railway login

# 4. Link to your Railway project
railway link

# 5. Set environment variables
railway variables set SECRET_KEY="$(openssl rand -hex 32)"
railway variables set JWT_SECRET_KEY="$(openssl rand -hex 32)"
railway variables set FLASK_ENV="production"
railway variables set DATABASE_URL="postgresql://postgres:sWzjTuwXcmRwdhpaokPNCPAASjjDfyQS@interchange.proxy.rlwy.net:23006/easy-download-db"

# 6. Deploy with Docker!
railway up

# 7. Check logs
railway logs

# 8. Get deployment URL
railway open
```

### Option 2: GitHub + Railway

```bash
# 1. Push to GitHub
cd "d:\Project\Youtube downloader\MainServer"
git init
git add .
git commit -m "Docker deployment ready"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main

# 2. In Railway Dashboard:
# - New Project → Deploy from GitHub
# - Select your repository
# - Railway will detect Dockerfile automatically
# - Set environment variables in Variables tab
# - Deploy!
```

---

## 🐳 Dockerfile Explanation

```dockerfile
FROM python:3.11-slim          # Lightweight Python base
WORKDIR /app                   # Set working directory

# Install FFmpeg for video processing
RUN apt-get update && apt-get install -y ffmpeg

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Create temp directories
RUN mkdir -p temp/singlelink temp/multilink temp/playlist

# Initialize database and start server
CMD python init_db.py && gunicorn app:app
```

### Key Features:
- ✅ **FFmpeg included** - For video/audio processing
- ✅ **Database auto-initialization** - Tables created on startup
- ✅ **Gunicorn server** - Production-ready WSGI server
- ✅ **4 workers** - Handles concurrent requests
- ✅ **300s timeout** - For long downloads
- ✅ **Optimized layers** - Fast builds with caching

---

## 🧪 Test Locally with Docker

### Build and Run

```bash
# Build the Docker image
docker build -t youtube-downloader .

# Run the container
docker run -p 5000:5000 \
  -e DATABASE_URL="postgresql://postgres:sWzjTuwXcmRwdhpaokPNCPAASjjDfyQS@interchange.proxy.rlwy.net:23006/easy-download-db" \
  -e SECRET_KEY="your-secret-key" \
  -e JWT_SECRET_KEY="your-jwt-key" \
  youtube-downloader
```

### Or use Docker Compose

```bash
# Create .env file with your variables
echo "DATABASE_URL=postgresql://postgres:sWzjTuwXcmRwdhpaokPNCPAASjjDfyQS@interchange.proxy.rlwy.net:23006/easy-download-db" > .env
echo "SECRET_KEY=your-secret-key" >> .env
echo "JWT_SECRET_KEY=your-jwt-key" >> .env

# Start with docker-compose
docker-compose up

# Stop
docker-compose down
```

### Test the API

```bash
# Health check
curl http://localhost:5000/health

# Database health
curl http://localhost:5000/api/database/health

# Register user
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "confirm_email": "test@example.com",
    "password": "TestPass123!",
    "confirm_password": "TestPass123!"
  }'
```

---

## ⚙️ Environment Variables for Railway

Set these in Railway Dashboard → Variables:

```bash
# Required
DATABASE_URL=postgresql://postgres:sWzjTuwXcmRwdhpaokPNCPAASjjDfyQS@interchange.proxy.rlwy.net:23006/easy-download-db
SECRET_KEY=<generate-random-32-char-string>
JWT_SECRET_KEY=<generate-random-32-char-string>

# Optional (with defaults)
FLASK_ENV=production
PORT=5000
YOUTUBE_TEMP_DIR=./temp
MAX_FILE_SIZE=524288000
MAX_CONCURRENT_DOWNLOADS=3
DOWNLOAD_TIMEOUT=300
CORS_ORIGINS=*
```

### Generate Secure Keys

**PowerShell:**
```powershell
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | % {[char]$_})
```

**Linux/Mac:**
```bash
openssl rand -hex 32
```

---

## 🔍 Verify Deployment

### 1. Check Build Logs

In Railway dashboard:
- Go to your service
- Click "Deployments"
- View build logs

Look for:
```
✅ Database tables created successfully!
[INFO] Booting worker with pid: ...
[INFO] Listening at: http://0.0.0.0:5000
```

### 2. Test Endpoints

```bash
# Replace with your Railway URL
RAILWAY_URL="https://your-app.railway.app"

# Health check
curl $RAILWAY_URL/health

# Database health
curl $RAILWAY_URL/api/database/health

# Register test user
curl -X POST $RAILWAY_URL/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "confirm_email": "test@example.com",
    "password": "TestPass123!",
    "confirm_password": "TestPass123!"
  }'
```

---

## 📊 Docker Image Details

### Image Size Optimization

- **Base image**: `python:3.11-slim` (~150MB)
- **With dependencies**: ~500MB
- **Final image**: ~550MB

### Included Packages

- ✅ Python 3.11
- ✅ Flask & Gunicorn
- ✅ yt-dlp (YouTube downloader)
- ✅ SQLAlchemy & psycopg2 (PostgreSQL)
- ✅ PyJWT & bcrypt (Authentication)
- ✅ FFmpeg (Video/audio processing)

### Excluded from Image

- ❌ Documentation (Summaries/)
- ❌ Git files
- ❌ Python cache
- ❌ Virtual environments
- ❌ Temporary files

---

## 🐛 Troubleshooting

### Issue 1: Database Connection Failed

**Error**: `connection to server failed`

**Solution**:
```bash
# Verify DATABASE_URL is set correctly
railway variables get DATABASE_URL

# Test connection
railway run python test_db_connection.py
```

### Issue 2: FFmpeg Not Found

**Error**: `ffmpeg: command not found`

**Solution**: FFmpeg is included in Dockerfile. Rebuild:
```bash
railway up --detach
```

### Issue 3: Port Binding Error

**Error**: `Address already in use`

**Solution**: Railway sets PORT automatically. Ensure app.py uses:
```python
port = int(os.getenv('PORT', 5000))
```

### Issue 4: Build Timeout

**Error**: `Build exceeded time limit`

**Solution**: Railway has generous build limits. If timeout occurs:
1. Check internet connection
2. Retry deployment
3. Contact Railway support

### Issue 5: Database Tables Not Created

**Error**: `relation "users" does not exist`

**Solution**:
```bash
# Manually initialize database
railway run python init_db.py
```

---

## 📈 Performance Optimization

### Current Configuration

```
Workers: 4
Timeout: 300 seconds
Max Concurrent Downloads: 3
Memory: ~512MB
```

### To Scale Up

**Increase Workers** (in Dockerfile):
```dockerfile
CMD gunicorn app:app --workers 8 --timeout 300
```

**Increase Concurrent Downloads**:
```bash
railway variables set MAX_CONCURRENT_DOWNLOADS=5
```

**Add Redis** (for caching):
```bash
railway add
# Select Redis
```

---

## 🔒 Security Best Practices

### ✅ Implemented

- ✅ Strong password requirements
- ✅ JWT token authentication
- ✅ Password hashing with bcrypt
- ✅ IP address tracking
- ✅ Environment variable secrets
- ✅ CORS configuration

### 🔧 Recommended

1. **Update secrets** in production:
   ```bash
   railway variables set SECRET_KEY="$(openssl rand -hex 32)"
   railway variables set JWT_SECRET_KEY="$(openssl rand -hex 32)"
   ```

2. **Set specific CORS origins**:
   ```bash
   railway variables set CORS_ORIGINS="https://your-frontend.com"
   ```

3. **Enable HTTPS only** (Railway does this automatically)

4. **Add rate limiting** (future enhancement)

---

## 📝 Deployment Checklist

### Pre-Deployment

- [x] Dockerfile created
- [x] .dockerignore configured
- [x] railway.json updated for Docker
- [x] docker-compose.yml for local testing
- [x] Database created and initialized
- [x] All tables verified

### Deployment

- [ ] Environment variables set in Railway
- [ ] Code pushed to GitHub (if using GitHub integration)
- [ ] Railway deployment triggered
- [ ] Build logs checked for errors
- [ ] Health endpoints tested

### Post-Deployment

- [ ] All API endpoints working
- [ ] User registration tested
- [ ] User login tested
- [ ] Video download tested
- [ ] Activity tracking verified
- [ ] Frontend updated with API URL

---

## 🎯 Quick Commands

```bash
# Build locally
docker build -t youtube-downloader .

# Run locally
docker run -p 5000:5000 youtube-downloader

# Deploy to Railway
railway up

# View logs
railway logs

# Check status
railway status

# Open dashboard
railway open

# Run command in Railway
railway run python init_db.py
```

---

## ✅ Ready to Deploy!

Your Docker configuration is complete and ready for Railway deployment!

### Next Steps:

1. **Set environment variables** in Railway dashboard
2. **Deploy**: `railway up`
3. **Verify**: Test health endpoints
4. **Update frontend** with Railway URL

---

## 📚 Additional Resources

- **Railway Docs**: https://docs.railway.app
- **Docker Docs**: https://docs.docker.com
- **Project Docs**: See `Summaries/` folder

---

**Your server is Docker-ready! Just run `railway up` to deploy! 🚀**
