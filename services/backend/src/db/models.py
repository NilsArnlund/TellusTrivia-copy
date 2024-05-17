from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    email = Column(String(50), nullable=True)
    password = Column(String(128), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    modified_at = Column(DateTime(timezone=True), server_onupdate=func.now(), server_default=func.now())
    profile_picture = Column(String(128), nullable=True)


class Game(Base):
    __tablename__ = 'game'

    game_id = Column(Integer, primary_key=True)
    pictures = Column(String(1000), default="")
    correct_current_guess = Column(String(3), default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Define relationship with GameState and add cascade='all, delete-orphan'
    game_states = relationship('GameState', back_populates='game', cascade='all, delete-orphan')


class GameState(Base):
    __tablename__ = 'game_state'

    game_id = Column(Integer, ForeignKey('game.game_id'), primary_key=True)
    player_id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    is_alive = Column(Boolean, default=True)
    has_guessed = Column(Boolean, default=False)
    current_guess = Column(String(3), default="")
    score = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_room_leader = Column(Boolean, default=False)
    
    game = relationship('Game', back_populates='game_states')


class Leaderboard(Base):
    __tablename__ = 'leaderboard'

    leaderboard_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    score = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    
