# verify_schema.py
import sys
import os
import importlib
from database.database import engine
import models.user

# Force reload
importlib.reload(models.user)
from models.user import User

from sqlalchemy import inspect
inspector = inspect(engine)

print("\n📋 VERIFIED Users table columns:")
columns = inspector.get_columns('users')
for col in columns:
    print(f"  • {col['name']}: {col['type']} | Nullable: {col['nullable']} | Default: {col['default']}")
    
    if col['name'] == 'is_active':
        if str(col['type']) == 'BOOLEAN':
            print("✅ is_active is correct BOOLEAN type")
        else:
            print(f"❌ is_active is {col['type']} - should be BOOLEAN")
            print("💡 The model change is not being applied!")
