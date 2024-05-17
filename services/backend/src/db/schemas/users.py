from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserIn(BaseModel):
    username: str
    email: str
    password: str

    class Config:
        orm_mode = True


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    created_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class UserDatabase(BaseModel):
    id: int
    username: str
    email: str
    password: str
    created_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None

    class Config:
        orm_mode = True
