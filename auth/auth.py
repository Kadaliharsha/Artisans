# auth/auth.py
"""
Authentication utilities for ArtisanHub
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

load_dotenv()

# Load secret and algorithm from environment
SECRET_KEY = os.getenv("SECRET_KEY", "change_this_in_production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Configure passlib to use bcrypt
from passlib.context import CryptContext

# Use bcrypt from passlib with explicit configuration
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12  # Standard rounds for bcrypt
)

# OAuth2 scheme for token extraction
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hash a password for storage
    """
    # Validate password length
    if len(password) > 72:
        raise ValueError("Password cannot be longer than 72 characters")
    
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[dict]:
    """
    Decode and validate a JWT token
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

# Add this test function
def test_hashing():
    """Test function to verify hashing works"""
    try:
        password = "test123"
        hashed = get_password_hash(password)
        print(f"Hashed: {hashed}")
        verified = verify_password(password, hashed)
        print(f"Verified: {verified}")
        return True
    except Exception as e:
        print(f"Hashing test failed: {e}")
        return False