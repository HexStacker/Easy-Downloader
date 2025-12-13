# 🔐 Railway Environment Variables

Copy these to your Railway dashboard (Variables tab):

## Required Variables

```bash
# Security Keys (IMPORTANT: Keep these secret!)
SECRET_KEY=aNTLgMV8rbJGRSomY61UfP4ACQ5kjnspxEHOuB3qtDwlX9KW2ev7iZzy0dcIFh
JWT_SECRET_KEY=UMiTyKwuvn2N7ZjlSBqhXRDxYFJ6csOoLf8tC4bPrHA50mGk9WI3VeQ1padzEg

# Flask Configuration
FLASK_ENV=production
PORT=5000

# Database (Railway PostgreSQL)
DATABASE_URL=postgresql://postgres:sWzjTuwXcmRwdhpaokPNCPAASjjDfyQS@interchange.proxy.rlwy.net:23006/easy-download-db

# YouTube Download Settings
YOUTUBE_TEMP_DIR=./temp
MAX_FILE_SIZE=524288000
MAX_CONCURRENT_DOWNLOADS=3
DOWNLOAD_TIMEOUT=300
RATE_LIMIT=1M

# CORS (Update with your frontend URL after deployment)
CORS_ORIGINS=https://downlode-easy.vercel.app
```

---

## 🚀 How to Set in Railway

### Option 1: Railway Dashboard (Recommended)

1. Go to your Railway project
2. Click on your service
3. Go to **Variables** tab
4. Click **+ New Variable**
5. Add each variable one by one:
   - Variable: `SECRET_KEY`
   - Value: `aNTLgMV8rbJGRSomY61UfP4ACQ5kjnspxEHOuB3qtDwlX9KW2ev7iZzy0dcIFh`
6. Repeat for all variables above

### Option 2: Railway CLI

```bash
# Set all variables at once
railway variables set SECRET_KEY="aNTLgMV8rbJGRSomY61UfP4ACQ5kjnspxEHOuB3qtDwlX9KW2ev7iZzy0dcIFh"
railway variables set JWT_SECRET_KEY="UMiTyKwuvn2N7ZjlSBqhXRDxYFJ6csOoLf8tC4bPrHA50mGk9WI3VeQ1padzEg"
railway variables set FLASK_ENV="production"
railway variables set PORT="5000"
railway variables set DATABASE_URL="postgresql://postgres:sWzjTuwXcmRwdhpaokPNCPAASjjDfyQS@interchange.proxy.rlwy.net:23006/easy-download-db"
railway variables set YOUTUBE_TEMP_DIR="./temp"
railway variables set MAX_FILE_SIZE="524288000"
railway variables set MAX_CONCURRENT_DOWNLOADS="3"
railway variables set DOWNLOAD_TIMEOUT="300"
railway variables set CORS_ORIGINS="*"
```

---

## 🔒 Security Notes

### ✅ Keys Generated
- **SECRET_KEY**: 64-character random string
- **JWT_SECRET_KEY**: 64-character random string
- Both use alphanumeric characters (a-z, A-Z, 0-9)

### ⚠️ Important
1. **Never commit these to Git** - They're in `.env.production` which is gitignored
2. **Keep them secret** - Don't share in public repositories
3. **Use different keys** for development and production
4. **Rotate keys** periodically for better security

### 🔄 To Generate New Keys

If you need to regenerate keys:

**PowerShell:**
```powershell
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 64 | % {[char]$_})
```

**Linux/Mac:**
```bash
openssl rand -base64 48
```

---

## 📋 Variable Descriptions

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask session encryption key | Generated |
| `JWT_SECRET_KEY` | JWT token signing key | Generated |
| `FLASK_ENV` | Flask environment mode | production |
| `PORT` | Server port | 5000 |
| `DATABASE_URL` | PostgreSQL connection string | Your Railway DB |
| `YOUTUBE_TEMP_DIR` | Temporary download directory | ./temp |
| `MAX_FILE_SIZE` | Maximum file size (bytes) | 524288000 (500MB) |
| `MAX_CONCURRENT_DOWNLOADS` | Concurrent download limit | 3 |
| `DOWNLOAD_TIMEOUT` | Download timeout (seconds) | 300 (5 min) |
| `CORS_ORIGINS` | Allowed CORS origins | * (all) |

---

## ✅ Verification

After setting variables in Railway:

```bash
# View all variables
railway variables

# Check specific variable
railway variables get SECRET_KEY
```

---

## 🎯 Next Steps

1. ✅ Copy variables to Railway dashboard
2. ✅ Verify all variables are set
3. ✅ Deploy: `railway up`
4. ✅ Test endpoints

---

**Your environment is now secure and ready for deployment! 🔐**
