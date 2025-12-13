# Easy Downloader Server

A modular Flask-based server for downloading YouTube videos with support for single links, multiple links, and playlists.

## 📁 Project Structure

```
MainServer/
├── AuthServer/          # Authentication module
│   ├── __init__.py
│   ├── routes.py       # Auth endpoints
│   └── service.py      # Auth business logic
├── YoutubeServer/       # YouTube download module
│   ├── singlelink/     # Single video downloads
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── service.py
│   ├── multilink/      # Batch downloads
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── service.py
│   ├── playlist/       # Playlist downloads
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── service.py
│   ├── __init__.py
│   ├── routes.py
│   └── config.py
├── DatabaseServer/      # Database module
│   ├── __init__.py
│   ├── config.py       # SQLAlchemy configuration
│   ├── models.py       # Database models
│   └── routes.py       # Database endpoints
├── app.py              # Main application
├── requirements.txt    # Dependencies
└── .env.example        # Environment variables template
```

## 🚀 Features

### YouTube Server
- **Single Link**: Download individual YouTube videos
- **Multi Link**: Batch download multiple videos
- **Playlist**: Download entire playlists with ZIP export

### Auth Server
- User registration and login
- JWT token-based authentication
- Token verification and logout

### Database Server
- PostgreSQL integration with SQLAlchemy
- Models for downloads, batches, playlists, and users
- Health check and initialization endpoints

## 📦 Installation

1. **Clone the repository**
```bash
cd MainServer
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Set up PostgreSQL database**
```bash
# Create database
createdb youtube_downloader

# Update DATABASE_URL in .env
DATABASE_URL=postgresql://username:password@localhost:5432/youtube_downloader
```

## 🏃 Running the Server

```bash
python app.py
```

Server will start on `http://localhost:5000`

## 📡 API Endpoints

### YouTube Server

#### Single Link
- `POST /api/youtube/single/info` - Get video information
- `POST /api/youtube/single/download` - Download single video
- `GET /api/youtube/single/status/<download_id>` - Get download status
- `GET /api/youtube/single/file/<download_id>` - Download file

#### Multi Link
- `POST /api/youtube/multi/batch` - Create batch download
- `GET /api/youtube/multi/batch/<batch_id>` - Get batch status
- `GET /api/youtube/multi/batch/<batch_id>/download` - Download batch as ZIP
- `POST /api/youtube/multi/batch/<batch_id>/cancel` - Cancel batch

#### Playlist
- `POST /api/youtube/playlist/info` - Get playlist information
- `POST /api/youtube/playlist/download` - Download playlist
- `GET /api/youtube/playlist/status/<playlist_id>` - Get playlist status
- `GET /api/youtube/playlist/download/<playlist_id>` - Download playlist as ZIP
- `POST /api/youtube/playlist/cancel/<playlist_id>` - Cancel playlist download

### Auth Server
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/verify` - Verify JWT token
- `POST /api/auth/logout` - Logout user
- `GET /api/auth/health` - Health check

### Database Server
- `GET /api/database/health` - Database health check
- `POST /api/database/init` - Initialize database tables

## 🔧 Configuration

Edit `.env` file:

```env
# Flask
SECRET_KEY=your-secret-key
PORT=5000

# JWT
JWT_SECRET_KEY=your-jwt-secret

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/youtube_downloader

# YouTube
MAX_CONCURRENT_DOWNLOADS=3
DOWNLOAD_TIMEOUT=300
```

## 📝 Example Usage

### Download Single Video
```bash
curl -X POST http://localhost:5000/api/youtube/single/download \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://youtube.com/watch?v=...",
    "format": "mp4",
    "quality": "720p"
  }'
```

### Create Batch Download
```bash
curl -X POST http://localhost:5000/api/youtube/multi/batch \
  -H "Content-Type: application/json" \
  -d '{
    "urls": ["url1", "url2", "url3"],
    "format": "mp4",
    "quality": "best"
  }'
```

### Download Playlist
```bash
curl -X POST http://localhost:5000/api/youtube/playlist/download \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://youtube.com/playlist?list=...",
    "format": "mp4",
    "quality": "1080p"
  }'
```

## 🛠️ Tech Stack

- **Flask** - Web framework
- **yt-dlp** - YouTube download library
- **SQLAlchemy** - ORM
- **PostgreSQL** - Database
- **JWT** - Authentication
- **bcrypt** - Password hashing

## 📄 License

MIT License

## 👨‍💻 Author

Easy Downloader Team
