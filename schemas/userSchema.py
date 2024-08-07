from pydantic import BaseModel,EmailStr, Field
from sqlalchemy import Column, Integer, String
from typing import List,Optional
class UserBase(BaseModel):
    name: str
    age: int
    gender: str
    email: EmailStr | None = Field(default=None)
    city: str
    interests: List[str]
class UserCreate(UserBase):
    email:str
class UserUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    email: Optional[str] = None
    city: Optional[str] = None
    interests: Optional[List[str]] = None
class Userr(UserBase):
    id: int

    class Config:
        from_attributes = True
