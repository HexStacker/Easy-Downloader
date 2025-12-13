"""
Database Initialization Script
Creates all tables in the PostgreSQL database
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from DatabaseServer.config import Base, engine, init_db
from DatabaseServer.models import (
    Download, Batch, BatchItem, Playlist, PlaylistItem, 
    User, UserActivity, DownloadStatus, DownloadType
)

def initialize_database():
    """Initialize all database tables"""
    try:
        print("🔄 Connecting to database...")
        print(f"Database URL: {os.getenv('DATABASE_URL', 'Not set')[:50]}...")
        
        print("\n🔄 Creating tables...")
        init_db()
        
        print("\n✅ Database tables created successfully!")
        print("\n📊 Created tables:")
        print("  - users")
        print("  - user_activities")
        print("  - downloads")
        print("  - batches")
        print("  - batch_items")
        print("  - playlists")
        print("  - playlist_items")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error initializing database: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Easy Downloader - Database Initialization")
    print("=" * 60)
    
    success = initialize_database()
    
    if success:
        print("\n" + "=" * 60)
        print("✅ Database is ready to use!")
        print("=" * 60)
        sys.exit(0)
    else:
        print("\n" + "=" * 60)
        print("❌ Database initialization failed!")
        print("=" * 60)
        sys.exit(1)
