# models/__init__.py
"""Initialize models package"""
from .base import Base
from .user import User
from .product import Product

# List of all models for easy reference
__all__ = ['Base', 'User', 'Product']