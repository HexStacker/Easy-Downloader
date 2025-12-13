"""
Database Connection Test Script
Tests connection to PostgreSQL database
"""

import os
import sys
from sqlalchemy import create_engine, text

def test_connection(database_url):
    """Test database connection"""
    try:
        print("🔄 Testing database connection...")
        print(f"URL: {database_url[:50]}...")
        
        # Create engine
        engine = create_engine(database_url, echo=False)
        
        # Test connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            print(f"\n✅ Connection successful!")
            print(f"PostgreSQL version: {version[:50]}...")
            
            # Test database name
            result = connection.execute(text("SELECT current_database();"))
            db_name = result.fetchone()[0]
            print(f"Database name: {db_name}")
            
            # List existing tables
            result = connection.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """))
            tables = result.fetchall()
            
            if tables:
                print(f"\nExisting tables ({len(tables)}):")
                for table in tables:
                    print(f"  - {table[0]}")
            else:
                print("\nNo tables found. Database is empty.")
            
        return True
        
    except Exception as e:
        print(f"\n❌ Connection failed!")
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Database Connection Test")
    print("=" * 60)
    
    # Get database URL from environment or argument
    database_url = os.getenv('DATABASE_URL')
    
    if len(sys.argv) > 1:
        database_url = sys.argv[1]
    
    if not database_url:
        print("\n❌ No database URL provided!")
        print("\nUsage:")
        print("  python test_db_connection.py <database-url>")
        print("  or set DATABASE_URL environment variable")
        sys.exit(1)
    
    success = test_connection(database_url)
    
    print("\n" + "=" * 60)
    if success:
        print("✅ Database connection test passed!")
        print("\nYou can now run: python init_db.py")
    else:
        print("❌ Database connection test failed!")
        print("\nPlease check:")
        print("  1. Database URL is correct")
        print("  2. Database server is running")
        print("  3. Credentials are valid")
        print("  4. Network allows connection")
    print("=" * 60)
    
    sys.exit(0 if success else 1)
