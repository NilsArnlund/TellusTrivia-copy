from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import and_
from .. import models

from datetime import datetime, timedelta

from src.db.schemas.leaderboard import LeaderboardEntryOut, LeaderboardOut

# create_leaderboard_entry
# if the user already ahs 20 entries if this one is within top 20 delete the worst one
async def create_leaderboard_entry(db: Session, username: str, score: int):
    new_leaderboard_entry = models.Leaderboard(
        username = username,
        score = score
    )

    db.add(new_leaderboard_entry)
    try:
        db.commit()
        db.refresh(new_leaderboard_entry)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Sorry, something went wrong with leaderboard entry")
    return LeaderboardEntryOut.from_orm(new_leaderboard_entry)


# get_leaderboard_entries_by_username
async def get_leaderboard_entries_by_username(db: Session, username: str):
    query_results = db.query(models.Leaderboard).filter(
        models.Leaderboard.username == username).order_by(
        models.Leaderboard.score.desc()).limit(20).all()

    return [LeaderboardOut.from_orm(entry) for entry in query_results]


# get_top_leaderboard_entries
async def get_top_leaderboard_entries(db: Session):
    query_results = db.query(models.Leaderboard).order_by(
        models.Leaderboard.score.desc()).limit(20).all()

    return [LeaderboardOut.from_orm(entry) for entry in query_results]


async def get_leaderboard_entries_by_date(db:Session):
    today_start = datetime.combine(datetime.today().date(), datetime.min.time())
    today_end = datetime.combine(datetime.today().date(), datetime.max.time())

    query_results = db.query(models.Leaderboard).filter(
        models.Leaderboard.created_at >= today_start,
        models.Leaderboard.created_at <= today_end
        ).order_by(models.Leaderboard.score.desc()).limit(10).all()

    return [LeaderboardOut.from_orm(entry) for entry in query_results]