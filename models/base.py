"""Use the single shared Base from the project's database module.

This ensures all models register with the same metadata object that
database.database uses when calling Base.metadata.create_all(engine).
"""
from database.database import Base