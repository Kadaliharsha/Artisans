from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: str
    
class UserCreate(UserBase):
    password: str
    role: Optional[str] = "customer"
    
class UserUpdate(UserBase):
    is_active: Optional[bool] = None
    role: Optional[str] = None
    
class User(UserBase):
    id: int
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True