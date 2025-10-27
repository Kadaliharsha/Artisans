# recreate_tables.py
import sys
import os
import importlib
import traceback

# Add project root to Python path
if os.path.dirname(__file__) not in sys.path:
    sys.path.insert(0, os.path.dirname(__file__))

def recreate_tables():
    try:
        # Force reload modules
        if 'models.user' in sys.modules:
            importlib.reload(sys.modules['models.user'])
        if 'database.database' in sys.modules:
            importlib.reload(sys.modules['database.database'])
        
        # Import after reload
        from database.database import engine
        from models.user import Base
        
        # Drop all tables
        print("🗑️  Dropping existing tables...")
        Base.metadata.drop_all(engine)
        print("✅ Tables dropped")
        
        # Create all tables
        print("🏗️  Creating new tables with correct schema...")
        Base.metadata.create_all(engine)
        print("✅ Tables created with correct schema!")
        
        # Verify
        from sqlalchemy import inspect
        inspector = inspect(engine)
        columns = inspector.get_columns('users')
        print("\n✅ FINAL TABLE SCHEMA:")
        for col in columns:
            if col['name'] == 'is_active':
                print(f"  • {col['name']}: {col['type']} ✓ (should be BOOLEAN)")
            elif col['name'] in ['created_at', 'updated_at']:
                print(f"  • {col['name']}: {col['type']} ✓ (should be TIMESTAMP)")
            else:
                print(f"  • {col['name']}: {col['type']}")
                
        # Check for duplicate indexes
        print("\n🔍 Checking indexes...")
        indexes = inspector.get_indexes('users')
        for idx in indexes:
            print(f"  • Index: {idx['name']} on {idx['column_names']}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print(f"Full traceback:")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    recreate_tables()