from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from models.user import User
from schemas.auth import Token, LoginRequest
from auth.auth import ( verify_password, create_access_token, get_password_hash, oauth2_scheme, decode_access_token )

from database.database import get_db
from schemas.user import User as UserSchema

router = APIRouter(prefix="/api/v1/auth")

@router.post("/login", response_model=Token)
def login(
    login_request: LoginRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == login_request.email).first()
    if not user or not verify_password(login_request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token_expires = timedelta(minutes=15)
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id, "role": user.role},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "role": user.role or "customer"
    }
    
@router.post("/register", response_model=UserSchema)
def register(
    email: str,
    password: str,
    role: str = "customer",
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.email == email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Validate password length
    if len(password) > 72:
        raise HTTPException(
            status_code=400,
            detail="Password cannot be longer than 72 characters"
        )
    try:    
        hashed_password = get_password_hash(password)
        db_user = User(
            email=email,
            hashed_password=hashed_password,
            role = role,
            is_active=True
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return db_user

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}"
        )
    
@router.get("/change-password")
def change_password(
    current_password: str,
    new_password: str,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    
    payload = decode_access_token(token)
    user_id = payload.get("user_id") if payload else None
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if not verify_password(current_password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid current password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user.hashed_password = get_password_hash(new_password)
    db.commit()

    return {"message": "Password changed successfully"}