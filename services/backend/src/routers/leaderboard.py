from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..db.crud import leaderboard_crud
from ..db.schemas.users import UserOut
from ..db.database import SessionLocal
from src.auth.jwthandler import (
    get_current_user,
)


router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/leaderboard/")
async def get_leaderboard(current_user: UserOut = Depends(get_current_user), db: Session = Depends(get_db)):
    leaderboard_entries = await leaderboard_crud.get_top_leaderboard_entries(db=db)

    if not leaderboard_entries:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No leaderboard entries found"
        )
    
    return leaderboard_entries


@router.get("/leaderboard/me")
async def get_leaderboard_me(current_user: UserOut = Depends(get_current_user), db: Session = Depends(get_db)):
    leaderboard_entries = await leaderboard_crud.get_leaderboard_entries_by_username(db=db, username=current_user.username)
    leaderboard_entries = leaderboard_entries[:10]

    if not leaderboard_entries:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No leaderboard entries found for user: {current_user.username}"
        )
    
    return leaderboard_entries


@router.get("/leaderboard/today")
async def get_leaderboard_today(current_user: UserOut = Depends(get_current_user), db: Session = Depends(get_db)):
    leaderboard_entries = await leaderboard_crud.get_leaderboard_entries_by_date(db=db)

    if not leaderboard_entries:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No leaderboard entries found for todays date."
        )
    
    return leaderboard_entries


@router.get("/leaderboard/{username}")
async def get_leaderboard_user(username: str, current_user: UserOut = Depends(get_current_user), db: Session = Depends(get_db)):
    leaderboard_entries = await leaderboard_crud.get_leaderboard_entries_by_username(db=db, username=username)

    if not leaderboard_entries:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No leaderboard entries found for user: {username}"
        )
    
    return leaderboard_entries
