from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class LeaderboardEntryOut(BaseModel):
    username: str
    score: int

    class Config:
        orm_mode = True


class LeaderboardOut(BaseModel):
    username: str  
    score: int  
    created_at: datetime  

    class Config:
        orm_mode = True