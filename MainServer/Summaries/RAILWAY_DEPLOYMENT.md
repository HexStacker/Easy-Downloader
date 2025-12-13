# Railway Deployment Guide

## 🚀 Step-by-Step Deployment

### Prerequisites
- Railway account
- PostgreSQL database already created on Railway
- Git repository (optional but recommended)

---

## 📋 Step 1: Verify Database Connection

The database URL you provided:
```
postgresql://easy-download:sWzjTuwXcmRwdhpaokPNCPAASjjDfyQS@interchange.proxy.rlwy.net:23006/easy-download-db
```

**⚠️ Note**: The connection failed with password authentication error. Please verify:

1. Go to your Railway PostgreSQL service
2. Click on "Variables" tab
3. Copy the correct `DATABASE_URL` or individual credentials:
   - `PGHOST`
   - `PGPORT`
   - `PGUSER`
   - `PGPASSWORD`
   - `PGDATABASE`

---

## 📋 Step 2: Update Environment Variables

Update `.env.production` with the correct database URL from Railway.

---

## 📋 Step 3: Initialize Database (Local Test)

```bash
# Set environment variable
$env:DATABASE_URL="postgresql://easy-download:sWzjTuwXcmRwdhpaokPNCPAASjjDfyQS@interchange.proxy.rlwy.net:23006/easy-download-db"

# Run initialization
python init_db.py
```

If successful, you should see:
```
✅ Database tables created successfully!
```

---

## 📋 Step 4: Deploy to Railway

### Option A: Using Railway CLI

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway**
   ```bash
   railway login
   ```

3. **Link to your project**
   ```bash
   cd MainServer
   railway link
   ```

4. **Set environment variables**
   ```bash
   railway variables set SECRET_KEY="your-secret-key-xyz123"
   railway variables set JWT_SECRET_KEY="your-jwt-secret-abc456"
   railway variables set FLASK_ENV="production"
   railway variables set PORT="5000"
   ```

5. **Deploy**
   ```bash
   railway up
   ```

### Option B: Using GitHub Integration

1. **Push code to GitHub**
   ```bash
   cd MainServer
   git init
   git add .
   git commit -m "Initial commit - YouTube Downloader Server"
   git branch -M main
   git remote add origin https://github.com/your-username/your-repo.git
   git push -u origin main
   ```

2. **Connect to Railway**
   - Go to Railway dashboard
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Select `MainServer` as root directory

3. **Configure Environment Variables**
   In Railway dashboard, go to your service → Variables tab:
   
   ```
   SECRET_KEY=your-secret-key-xyz123
   JWT_SECRET_KEY=your-jwt-secret-abc456
   FLASK_ENV=production
   PORT=5000
   DATABASE_URL=${{Postgres.DATABASE_URL}}
   ```

4. **Deploy**
   - Railway will automatically deploy
   - Database will be initialized on first deployment

### Option C: Manual Deployment

1. **Create new service on Railway**
   - Go to Railway dashboard
   - Click "New Project" → "Empty Project"
   - Click "New" → "Empty Service"

2. **Configure service**
   - Settings → Environment: Select your PostgreSQL database
   - Settings → Variables: Add all environment variables

3. **Deploy from local**
   ```bash
   railway link
   railway up
   ```

---

## 📋 Step 5: Verify Deployment

1. **Check logs**
   ```bash
   railway logs
   ```

2. **Test health endpoint**
   ```bash
   curl https://your-app.railway.app/health
   ```

3. **Test database endpoint**
   ```bash
   curl https://your-app.railway.app/api/database/health
   ```

---

## 🔧 Environment Variables Checklist

Make sure these are set in Railway:

- [ ] `SECRET_KEY` - Flask secret key
- [ ] `JWT_SECRET_KEY` - JWT signing key
- [ ] `FLASK_ENV` - Set to "production"
- [ ] `PORT` - Set to 5000 (or use Railway's $PORT)
- [ ] `DATABASE_URL` - PostgreSQL connection string
- [ ] `YOUTUBE_TEMP_DIR` - Set to "./temp"
- [ ] `MAX_CONCURRENT_DOWNLOADS` - Set to 3
- [ ] `CORS_ORIGINS` - Set to your frontend URL or "*"

---

## 📊 Database Tables

The following tables will be created automatically:

1. **users** - User accounts
2. **user_activities** - Download history
3. **downloads** - Individual downloads
4. **batches** - Batch downloads
5. **batch_items** - Items in batches
6. **playlists** - Playlist downloads
7. **playlist_items** - Videos in playlists

---

## 🐛 Troubleshooting

### Database Connection Failed

**Error**: `password authentication failed`

**Solution**:
1. Go to Railway PostgreSQL service
2. Copy the correct `DATABASE_URL` from Variables tab
3. Update your environment variables
4. Redeploy

### Tables Not Created

**Error**: Tables don't exist

**Solution**:
```bash
# Manually run initialization
railway run python init_db.py
```

### Port Already in Use

**Error**: `Address already in use`

**Solution**:
- Railway automatically assigns a port
- Make sure your app uses `os.getenv('PORT', 5000)`

### Import Errors

**Error**: `ModuleNotFoundError`

**Solution**:
- Ensure `requirements.txt` is complete
- Railway will install dependencies automatically

---

## 📝 Post-Deployment Checklist

- [ ] Database initialized successfully
- [ ] Health endpoint responding
- [ ] Can register a user
- [ ] Can login
- [ ] Can download a video
- [ ] Activity is being tracked
- [ ] Logs are clean

---

## 🔗 Useful Commands

```bash
# View logs
railway logs

# Run command in Railway environment
railway run python init_db.py

# Open Railway dashboard
railway open

# Check service status
railway status

# Set variable
railway variables set KEY=value

# Get variable
railway variables get KEY
```

---

## 🌐 API Endpoints

Once deployed, your API will be available at:

```
https://your-app.railway.app/

Endpoints:
- GET  /health
- POST /api/auth/register
- POST /api/auth/login
- GET  /api/auth/profile
- GET  /api/auth/activity
- POST /api/youtube/single/download
- POST /api/youtube/multi/batch
- POST /api/youtube/playlist/download
```

---

## 📞 Need Help?

1. Check Railway logs: `railway logs`
2. Check database connection in Railway dashboard
3. Verify environment variables are set correctly
4. Test database connection locally first

---

## ✅ Success Indicators

You'll know deployment is successful when:

1. ✅ `railway logs` shows "Database initialized successfully"
2. ✅ Health endpoint returns `{"status": "healthy"}`
3. ✅ Database health returns `{"connected": true}`
4. ✅ You can register and login
5. ✅ Downloads work and are tracked

---

## 🎉 Next Steps After Deployment

1. **Update Frontend**
   - Update API URL to Railway deployment URL
   - Test all features

2. **Monitor**
   - Check Railway metrics
   - Monitor database usage
   - Review logs regularly

3. **Secure**
   - Update SECRET_KEY and JWT_SECRET_KEY to strong random values
   - Set CORS_ORIGINS to your frontend domain
   - Enable HTTPS only

4. **Scale**
   - Adjust worker count in Procfile if needed
   - Monitor response times
   - Add caching if necessary
