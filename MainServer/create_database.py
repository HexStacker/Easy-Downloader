"""
Create Database Script
First creates the database, then initializes tables
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError

def create_database(base_url, db_name):
    """Create the database if it doesn't exist"""
    try:
        # Connect to postgres database (default)
        postgres_url = base_url.rsplit('/', 1)[0] + '/postgres'
        print(f"🔄 Connecting to PostgreSQL server...")
        print(f"URL: {postgres_url[:50]}...")
        
        engine = create_engine(postgres_url, isolation_level="AUTOCOMMIT")
        
        with engine.connect() as connection:
            # Check if database exists
            result = connection.execute(text(
                f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'"
            ))
            exists = result.fetchone()
            
            if exists:
                print(f"\n✅ Database '{db_name}' already exists!")
                return True
            
            # Create database
            print(f"\n🔄 Creating database '{db_name}'...")
            connection.execute(text(f'CREATE DATABASE "{db_name}"'))
            print(f"✅ Database '{db_name}' created successfully!")
            
        return True
        
    except Exception as e:
        print(f"\n❌ Error creating database: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def initialize_tables(database_url):
    """Initialize all tables"""
    try:
        print(f"\n🔄 Connecting to database...")
        
        # Import after database is created
        from DatabaseServer.config import Base, engine, init_db
        from DatabaseServer.models import (
            Download, Batch, BatchItem, Playlist, PlaylistItem, 
            User, UserActivity
        )
        
        print("🔄 Creating tables...")
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
        
        # Verify tables
        with engine.connect() as connection:
            result = connection.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """))
            tables = result.fetchall()
            
            print(f"\n✅ Verified {len(tables)} tables in database:")
            for table in tables:
                print(f"  ✓ {table[0]}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error initializing tables: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Easy Downloader - Database Setup")
    print("=" * 60)
    
    # Get database URL
    database_url = os.getenv('DATABASE_URL')
    
    if len(sys.argv) > 1:
        database_url = sys.argv[1]
    
    if not database_url:
        print("\n❌ No database URL provided!")
        print("\nUsage:")
        print("  python create_database.py <database-url>")
        print("  or set DATABASE_URL environment variable")
        sys.exit(1)
    
    # Extract database name
    db_name = database_url.rsplit('/', 1)[-1]
    
    print(f"\nDatabase name: {db_name}")
    print(f"Database URL: {database_url[:50]}...")
    
    # Step 1: Create database
    print("\n" + "=" * 60)
    print("Step 1: Create Database")
    print("=" * 60)
    
    if not create_database(database_url, db_name):
        print("\n❌ Failed to create database!")
        sys.exit(1)
    
    # Step 2: Initialize tables
    print("\n" + "=" * 60)
    print("Step 2: Initialize Tables")
    print("=" * 60)
    
    if not initialize_tables(database_url):
        print("\n❌ Failed to initialize tables!")
        sys.exit(1)
    
    # Success
    print("\n" + "=" * 60)
    print("✅ Database setup complete!")
    print("=" * 60)
    print(f"\nDatabase '{db_name}' is ready to use!")
    print("\nYou can now:")
    print("  1. Start the server: python app.py")
    print("  2. Deploy to Railway: railway up")
    print("=" * 60)
    
    sys.exit(0)
