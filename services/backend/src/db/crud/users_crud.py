from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from sqlalchemy import and_

import random

from .. import models 
from src.db.schemas.users import UserIn, UserOut

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


async def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


async def get_user_by_id(db: Session, id: int):
    return db.query(models.User).filter(models.User.id == id).first()


async def create_user(db: Session, user: UserIn) -> UserOut:
    # Encrypt the user's password
    user.password = pwd_context.hash(user.password)

    profile_picture = "default" + str(random.randint(0,9)) + ".png"

    # Create a new user instance
    new_user = models.User(
        username=user.username,
        password=user.password,
        email=user.email,
        profile_picture=profile_picture
    )
    
    # Add the new user to the session and commit
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=401, detail=f"Sorry, that user already exists.")

    # Convert the new user object to UserOutSchema and return it
    return UserOut.from_orm(new_user)


# update user profile picture
async def update_user_profile_picture(db: Session, username: str, filename: str):
    user = db.query(models.User).filter(models.User.username == username).first()

    if user:
        if user.profile_picture:
            user.profile_picture = filename
        
        try:
            db.commit()
            db.refresh(user)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"An error occurred while modifying the picture: {e}")
    else:
        raise HTTPException(status_code=404, detail=f"User with username {username} not found")
    return


async def update_user_password(db: Session, username: str, password: str):
    user = db.query(models.User).filter(models.User.username == username).first()

    if user:
        if user.password:
            user.password = password
        
        try:
            db.commit()
            db.refresh(user)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"An error occurred while updating the password")
    else:
        raise HTTPException(status_code=404, detail=f"User with username {username} not found")
    return


async def get_user_profile_picture(db : Session, username : str):
    user = db.query(models.User).filter(models.User.username == username).first()
    return user.profile_picture