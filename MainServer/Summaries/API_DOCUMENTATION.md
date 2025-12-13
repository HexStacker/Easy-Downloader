# API Documentation

## Base URL
```
http://localhost:5000
```

## Authentication
Most endpoints require JWT authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

---

## 🎬 YouTube Server API

### Single Link Downloads

#### Get Video Information
```http
POST /api/youtube/single/info
Content-Type: application/json

{
  "url": "https://youtube.com/watch?v=dQw4w9WgXcQ"
}
```

**Response:**
```json
{
  "success": true,
  "title": "Video Title",
  "duration": 213,
  "thumbnail": "https://...",
  "uploader": "Channel Name",
  "view_count": 1000000,
  "formats": {
    "video": [...],
    "audio": [...]
  }
}
```

#### Download Single Video
```http
POST /api/youtube/single/download
Content-Type: application/json

{
  "url": "https://youtube.com/watch?v=dQw4w9WgXcQ",
  "format": "mp4",
  "quality": "720p"
}
```

**Parameters:**
- `url` (required): YouTube video URL
- `format` (optional): "mp4" or "mp3" (default: "mp4")
- `quality` (optional): "best", "2160p", "1440p", "1080p", "720p", "480p", "360p" (default: "best")

**Response:**
```json
{
  "success": true,
  "download_id": "uuid-here",
  "message": "Download started"
}
```

#### Get Download Status
```http
GET /api/youtube/single/status/<download_id>
```

**Response:**
```json
{
  "id": "uuid-here",
  "status": "completed",
  "progress": 100,
  "title": "Video Title",
  "filename": "video.mp4",
  "file_path": "/path/to/file"
}
```

#### Download File
```http
GET /api/youtube/single/file/<download_id>
```

Returns the video file as attachment.

---

### Multi Link (Batch) Downloads

#### Create Batch Download
```http
POST /api/youtube/multi/batch
Content-Type: application/json

{
  "urls": [
    "https://youtube.com/watch?v=...",
    "https://youtube.com/watch?v=...",
    "https://youtube.com/watch?v=..."
  ],
  "format": "mp4",
  "quality": "best"
}
```

**Parameters:**
- `urls` (required): Array of YouTube URLs (max 50)
- `format` (optional): "mp4" or "mp3"
- `quality` (optional): Video quality

**Response:**
```json
{
  "success": true,
  "batch_id": "uuid-here",
  "total_videos": 3,
  "message": "Batch download created"
}
```

#### Get Batch Status
```http
GET /api/youtube/multi/batch/<batch_id>
```

**Response:**
```json
{
  "batch_id": "uuid-here",
  "status": "downloading",
  "total": 3,
  "completed": 2,
  "failed": 0,
  "progress": 66,
  "videos": [...]
}
```

#### Download Batch as ZIP
```http
GET /api/youtube/multi/batch/<batch_id>/download
```

Returns all videos in a ZIP file.

#### Cancel Batch
```http
POST /api/youtube/multi/batch/<batch_id>/cancel
```

**Response:**
```json
{
  "success": true,
  "message": "Batch cancelled"
}
```

---

### Playlist Downloads

#### Get Playlist Information
```http
POST /api/youtube/playlist/info
Content-Type: application/json

{
  "url": "https://youtube.com/playlist?list=..."
}
```

**Response:**
```json
{
  "success": true,
  "title": "Playlist Title",
  "uploader": "Channel Name",
  "video_count": 25,
  "videos": [
    {
      "id": "video-id",
      "title": "Video Title",
      "duration": 213,
      "url": "https://..."
    }
  ]
}
```

#### Download Playlist
```http
POST /api/youtube/playlist/download
Content-Type: application/json

{
  "url": "https://youtube.com/playlist?list=...",
  "format": "mp4",
  "quality": "720p",
  "start_index": 1,
  "end_index": 10
}
```

**Parameters:**
- `url` (required): YouTube playlist URL
- `format` (optional): "mp4" or "mp3"
- `quality` (optional): Video quality
- `start_index` (optional): Start from this video (1-based)
- `end_index` (optional): End at this video (1-based)

**Response:**
```json
{
  "success": true,
  "playlist_id": "uuid-here",
  "total_videos": 10,
  "message": "Playlist download started"
}
```

#### Get Playlist Status
```http
GET /api/youtube/playlist/status/<playlist_id>
```

**Response:**
```json
{
  "playlist_id": "uuid-here",
  "title": "Playlist Title",
  "status": "downloading",
  "total": 10,
  "completed": 7,
  "failed": 0,
  "progress": 70,
  "videos": [...]
}
```

#### Download Playlist as ZIP
```http
GET /api/youtube/playlist/download/<playlist_id>
```

Returns all playlist videos in a ZIP file.

#### Cancel Playlist Download
```http
POST /api/youtube/playlist/cancel/<playlist_id>
```

---

## 🔐 Authentication API

### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securePassword123"
}
```

**Response:**
```json
{
  "success": true,
  "message": "User registered successfully",
  "user_id": 1
}
```

### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "securePassword123"
}
```

**Response:**
```json
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  }
}
```

### Verify Token
```http
POST /api/auth/verify
Authorization: Bearer <token>
```

**Response:**
```json
{
  "valid": true,
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  }
}
```

### Logout
```http
POST /api/auth/logout
Authorization: Bearer <token>
```

**Response:**
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

---

## 🗄️ Database API

### Health Check
```http
GET /api/database/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "database-server",
  "database": "postgresql",
  "connected": true
}
```

### Initialize Database
```http
POST /api/database/init
```

**Response:**
```json
{
  "success": true,
  "message": "Database tables created successfully"
}
```

---

## 📊 Status Codes

- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid request parameters
- `401 Unauthorized` - Authentication required or failed
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

---

## 🔄 Download Status Values

- `pending` - Download queued
- `downloading` - Download in progress
- `completed` - Download finished successfully
- `failed` - Download failed
- `cancelled` - Download cancelled by user

---

## 💡 Usage Examples

### Python
```python
import requests

# Download single video
response = requests.post(
    'http://localhost:5000/api/youtube/single/download',
    json={
        'url': 'https://youtube.com/watch?v=...',
        'format': 'mp4',
        'quality': '720p'
    }
)
download_id = response.json()['download_id']

# Check status
status = requests.get(
    f'http://localhost:5000/api/youtube/single/status/{download_id}'
)
print(status.json())
```

### JavaScript
```javascript
// Download single video
const response = await fetch('http://localhost:5000/api/youtube/single/download', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    url: 'https://youtube.com/watch?v=...',
    format: 'mp4',
    quality: '720p'
  })
});

const { download_id } = await response.json();

// Check status
const statusResponse = await fetch(
  `http://localhost:5000/api/youtube/single/status/${download_id}`
);
const status = await statusResponse.json();
console.log(status);
```

### cURL
```bash
# Download single video
curl -X POST http://localhost:5000/api/youtube/single/download \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://youtube.com/watch?v=...",
    "format": "mp4",
    "quality": "720p"
  }'

# Check status
curl http://localhost:5000/api/youtube/single/status/<download_id>
```
