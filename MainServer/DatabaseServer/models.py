"""
Database Models
SQLAlchemy models for the application
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from .config import Base

class DownloadStatus(enum.Enum):
    """Download status enumeration"""
    PENDING = "pending"
    DOWNLOADING = "downloading"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class DownloadType(enum.Enum):
    """Download type enumeration"""
    SINGLE = "single"
    BATCH = "batch"
    PLAYLIST = "playlist"

class Download(Base):
    """Download model for tracking all downloads"""
    __tablename__ = "downloads"
    
    id = Column(String, primary_key=True)
    type = Column(Enum(DownloadType), nullable=False)
    status = Column(Enum(DownloadStatus), default=DownloadStatus.PENDING)
    
    # Download details
    url = Column(Text, nullable=False)
    title = Column(String(500))
    format = Column(String(10))  # mp4, mp3
    quality = Column(String(20))  # best, 720p, 1080p, etc.
    
    # Progress tracking
    progress = Column(Float, default=0.0)
    total_size = Column(Integer)  # in bytes
    downloaded_size = Column(Integer, default=0)
    
    # File information
    file_path = Column(Text)
    filename = Column(String(500))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    
    # Error handling
    error_message = Column(Text)
    
    # Relationships
    batch_items = relationship("BatchItem", back_populates="download")
    playlist_items = relationship("PlaylistItem", back_populates="download")

class Batch(Base):
    """Batch download model"""
    __tablename__ = "batches"
    
    id = Column(String, primary_key=True)
    status = Column(Enum(DownloadStatus), default=DownloadStatus.PENDING)
    
    # Batch details
    total_videos = Column(Integer)
    completed_videos = Column(Integer, default=0)
    failed_videos = Column(Integer, default=0)
    progress = Column(Float, default=0.0)
    
    # Settings
    format = Column(String(10))
    quality = Column(String(20))
    
    # File information
    zip_path = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    # Relationships
    items = relationship("BatchItem", back_populates="batch")

class BatchItem(Base):
    """Individual items in a batch download"""
    __tablename__ = "batch_items"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    batch_id = Column(String, ForeignKey("batches.id"))
    download_id = Column(String, ForeignKey("downloads.id"))
    
    url = Column(Text, nullable=False)
    order = Column(Integer)  # Order in batch
    
    # Relationships
    batch = relationship("Batch", back_populates="items")
    download = relationship("Download", back_populates="batch_items")

class Playlist(Base):
    """Playlist download model"""
    __tablename__ = "playlists"
    
    id = Column(String, primary_key=True)
    status = Column(Enum(DownloadStatus), default=DownloadStatus.PENDING)
    
    # Playlist details
    url = Column(Text, nullable=False)
    title = Column(String(500))
    uploader = Column(String(200))
    total_videos = Column(Integer)
    completed_videos = Column(Integer, default=0)
    failed_videos = Column(Integer, default=0)
    progress = Column(Float, default=0.0)
    
    # Settings
    format = Column(String(10))
    quality = Column(String(20))
    start_index = Column(Integer)
    end_index = Column(Integer)
    
    # File information
    zip_path = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    # Relationships
    items = relationship("PlaylistItem", back_populates="playlist")

class PlaylistItem(Base):
    """Individual videos in a playlist"""
    __tablename__ = "playlist_items"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    playlist_id = Column(String, ForeignKey("playlists.id"))
    download_id = Column(String, ForeignKey("downloads.id"))
    
    url = Column(Text, nullable=False)
    title = Column(String(500))
    index = Column(Integer)  # Position in playlist
    duration = Column(Integer)  # in seconds
    
    # Relationships
    playlist = relationship("Playlist", back_populates="items")
    download = relationship("Download", back_populates="playlist_items")

class User(Base):
    """User model for authentication"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    
    # IP tracking
    registration_ip = Column(String(50))
    last_login_ip = Column(String(50))
    last_login_at = Column(DateTime)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    activities = relationship("UserActivity", back_populates="user")

class UserActivity(Base):
    """User activity tracking - records all user downloads"""
    __tablename__ = "user_activities"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Activity details
    activity_type = Column(Enum(DownloadType), nullable=False)  # single, batch, playlist
    download_id = Column(String, nullable=False)  # Reference to download/batch/playlist ID
    
    # Download information
    url = Column(Text, nullable=False)
    title = Column(String(500))
    format = Column(String(10))  # mp4, mp3
    quality = Column(String(20))  # best, 720p, etc.
    
    # Status tracking
    status = Column(Enum(DownloadStatus), default=DownloadStatus.PENDING)
    
    # IP and timestamp
    ip_address = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    # File information
    file_size = Column(Integer)  # in bytes
    file_path = Column(Text)
    
    # Additional metadata
    user_agent = Column(String(500))  # Browser/client info
    
    # Relationships
    user = relationship("User", back_populates="activities")

