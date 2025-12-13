# System Architecture

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend (React)                         │
│                    http://localhost:3000                         │
└────────────────────────┬────────────────────────────────────────┘
                         │ HTTP/REST API
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      MainServer (Flask)                          │
│                    http://localhost:5000                         │
│                                                                   │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐         │
│  │ AuthServer  │  │YoutubeServer │  │ DatabaseServer │         │
│  │             │  │              │  │                │         │
│  │ - Register  │  │ - Single     │  │ - PostgreSQL   │         │
│  │ - Login     │  │ - Multi      │  │ - Models       │         │
│  │ - Verify    │  │ - Playlist   │  │ - Health       │         │
│  │ - Logout    │  │              │  │                │         │
│  └─────────────┘  └──────────────┘  └────────────────┘         │
│                           │                    │                 │
└───────────────────────────┼────────────────────┼─────────────────┘
                            │                    │
                            ▼                    ▼
                    ┌──────────────┐    ┌──────────────┐
                    │   yt-dlp     │    │  PostgreSQL  │
                    │   Library    │    │   Database   │
                    └──────────────┘    └──────────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │   YouTube    │
                    │   Platform   │
                    └──────────────┘
```

## 📊 Module Breakdown

### 1. YoutubeServer Module
```
YoutubeServer/
├── singlelink/          # Single video downloads
│   ├── routes.py        # API endpoints
│   └── service.py       # Business logic
│
├── multilink/           # Batch downloads
│   ├── routes.py        # Batch API
│   └── service.py       # Concurrent processing
│
└── playlist/            # Playlist downloads
    ├── routes.py        # Playlist API
    └── service.py       # Playlist processing
```

**Flow:**
```
Client Request → Routes → Service → yt-dlp → YouTube → Download → Response
```

### 2. AuthServer Module
```
AuthServer/
├── routes.py            # Auth endpoints
└── service.py           # JWT & bcrypt logic
```

**Flow:**
```
Register: Client → Hash Password → Store User → Response
Login:    Client → Verify Password → Generate JWT → Response
Verify:   Client → Validate JWT → Extract User → Response
```

### 3. DatabaseServer Module
```
DatabaseServer/
├── config.py            # SQLAlchemy setup
├── models.py            # ORM models
└── routes.py            # DB endpoints
```

**Models:**
- Download (single downloads)
- Batch (batch downloads)
- BatchItem (items in batch)
- Playlist (playlist downloads)
- PlaylistItem (videos in playlist)
- User (authentication)

## 🔄 Request Flow Examples

### Single Video Download
```
1. Client sends POST /api/youtube/single/download
   ↓
2. Routes validates request
   ↓
3. Service extracts video info via yt-dlp
   ↓
4. Service starts download
   ↓
5. Download saved to temp/singlelink/
   ↓
6. Response with download_id
   ↓
7. Client polls GET /api/youtube/single/status/<id>
   ↓
8. Client downloads GET /api/youtube/single/file/<id>
```

### Batch Download
```
1. Client sends POST /api/youtube/multi/batch with URLs array
   ↓
2. Routes validates (max 50 URLs)
   ↓
3. Service creates batch job
   ↓
4. ThreadPoolExecutor spawns 3 workers
   ↓
5. Each worker downloads video concurrently
   ↓
6. Progress updated in real-time
   ↓
7. All videos saved to temp/multilink/<batch_id>/
   ↓
8. Client requests GET /api/youtube/multi/batch/<id>/download
   ↓
9. Service creates ZIP file
   ↓
10. ZIP file sent to client
```

### Playlist Download
```
1. Client sends POST /api/youtube/playlist/info
   ↓
2. Service extracts playlist metadata
   ↓
3. Returns list of videos
   ↓
4. Client sends POST /api/youtube/playlist/download
   ↓
5. Service processes videos with index ordering
   ↓
6. Files named: 001_title.mp4, 002_title.mp4, etc.
   ↓
7. Progress tracked per video
   ↓
8. ZIP created with ordered files
   ↓
9. Client downloads ZIP
```

## 🔐 Authentication Flow
```
Register:
Client → POST /api/auth/register
       → bcrypt.hashpw(password)
       → Store in database/memory
       → Return user_id

Login:
Client → POST /api/auth/login
       → Verify password with bcrypt
       → Generate JWT token
       → Return token + user info

Protected Request:
Client → Request with Authorization: Bearer <token>
       → Verify JWT signature
       → Extract user from payload
       → Process request
       → Return response
```

## 💾 Database Schema

```sql
-- Downloads table
downloads (
  id VARCHAR PRIMARY KEY,
  type ENUM('single', 'batch', 'playlist'),
  status ENUM('pending', 'downloading', 'completed', 'failed', 'cancelled'),
  url TEXT,
  title VARCHAR(500),
  format VARCHAR(10),
  quality VARCHAR(20),
  progress FLOAT,
  file_path TEXT,
  created_at TIMESTAMP,
  completed_at TIMESTAMP
)

-- Batches table
batches (
  id VARCHAR PRIMARY KEY,
  status ENUM(...),
  total_videos INTEGER,
  completed_videos INTEGER,
  failed_videos INTEGER,
  progress FLOAT,
  zip_path TEXT,
  created_at TIMESTAMP
)

-- Playlists table
playlists (
  id VARCHAR PRIMARY KEY,
  url TEXT,
  title VARCHAR(500),
  total_videos INTEGER,
  completed_videos INTEGER,
  progress FLOAT,
  zip_path TEXT,
  created_at TIMESTAMP
)

-- Users table
users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(100) UNIQUE,
  email VARCHAR(200) UNIQUE,
  password_hash VARCHAR(255),
  is_active BOOLEAN,
  created_at TIMESTAMP
)
```

## 🌐 API Endpoint Map

```
/                                    # API info
/health                              # Health check

/api/youtube/health                  # YouTube server health
/api/youtube/single/*                # Single video operations
/api/youtube/multi/*                 # Batch operations
/api/youtube/playlist/*              # Playlist operations

/api/auth/register                   # User registration
/api/auth/login                      # User login
/api/auth/verify                     # Token verification
/api/auth/logout                     # User logout
/api/auth/health                     # Auth server health

/api/database/health                 # Database health
/api/database/init                   # Initialize tables
```

## 🚀 Scalability Considerations

### Current Implementation
- In-memory storage (dict)
- 3 concurrent workers
- Local file system

### Production Recommendations
1. **Replace in-memory storage** with PostgreSQL
2. **Use Celery** for background tasks
3. **Add Redis** for caching and queues
4. **Use S3/Cloud Storage** for files
5. **Add rate limiting** per user
6. **Implement websockets** for real-time progress
7. **Add monitoring** (Prometheus, Grafana)
8. **Load balancing** with multiple instances

### Future Platform Support
```
MainServer/
├── YoutubeServer/
├── InstagramServer/     # Future
├── TikTokServer/        # Future
├── TwitterServer/       # Future
└── FacebookServer/      # Future
```

Each platform server follows the same pattern:
- `routes.py` - API endpoints
- `service.py` - Business logic
- `config.py` - Configuration

## 📈 Performance Metrics

- **Concurrent Downloads**: 3 simultaneous
- **Max Batch Size**: 50 URLs
- **Download Timeout**: 300 seconds
- **Max File Size**: 500MB
- **JWT Expiry**: 7 days

## 🔧 Technology Stack

| Layer | Technology |
|-------|-----------|
| Web Framework | Flask 3.0 |
| Download Engine | yt-dlp |
| Database | PostgreSQL + SQLAlchemy |
| Authentication | JWT + bcrypt |
| Concurrency | ThreadPoolExecutor |
| Production Server | Gunicorn |
| CORS | Flask-CORS |

## 🎯 Design Principles

1. **Separation of Concerns** - Each module has a single responsibility
2. **Modularity** - Easy to add new platforms
3. **Scalability** - Concurrent processing, database persistence
4. **Security** - JWT auth, password hashing, input validation
5. **Maintainability** - Clear structure, comprehensive docs
6. **Production Ready** - Error handling, logging, deployment configs
