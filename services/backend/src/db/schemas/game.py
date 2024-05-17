from typing import Optional
from pydantic import BaseModel


class GameOut(BaseModel):
    game_id: int
    pictures: str

    class Config:
        orm_mode = True


class GameStateOut(BaseModel):
    game_id: int
    player_id: int

    class Config:
        orm_mode = True