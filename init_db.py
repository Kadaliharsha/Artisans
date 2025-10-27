"""
Initialize the database with all tables
This script creates all tables defined in the models
"""

from sqlalchemy import create_engine, inspect, text
import os
from dotenv import load_dotenv

# Import models - this is crucial for Base.metadata to know about them
from models.user import User
from models.base import Base

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env file")

# Create engine
engine = create_engine(
    DATABASE_URL,
    echo=True  # This will show SQL statements for debugging
)

def initialize_database():
    """
    Initialize the database by creating all tables
    """
    try:
        # Test connection first
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1")).fetchone()
            print(f"✅ Connection successful: {result[0]}")
            
        # Create all tables
        # This will create tables in the public schema automatically
        Base.metadata.create_all(engine)
        print("✅ Database initialization completed!")
        
        # Verify what was created
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"📊 Tables created: {tables}")
        
        if tables:
            print("\n📋 Table details:")
            for table in tables:
                columns = inspector.get_columns(table)
                print(f"  • {table} ({len(columns)} columns)")
                for col in columns:
                    pk = " 🔑" if col.get('primary_key') else ""
                    idx = " 🏷️" if col.get('index') else ""
                    print(f"    - {col['name']} ({col['type']}){pk}{idx}")
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        print(f"💡 Error type: {type(e).__name__}")
        
        # Provide specific help based on error
        if "password" in str(e).lower():
            print("💡 Check your password in .env file")
        elif "database" in str(e).lower():
            print("💡 Database might not exist or wrong name")
        elif "connection" in str(e).lower():
            print("💡 PostgreSQL might not be running")

if __name__ == "__main__":
    print("🚀 Starting database initialization...")
    initialize_database()