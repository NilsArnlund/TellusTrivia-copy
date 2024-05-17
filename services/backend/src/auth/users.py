from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy.orm import Session
import random
import string

from src.db.crud import users_crud

from src.db.database import SessionLocal
from src.db.schemas.users import UserOut


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def generate_random_password(length=5):
    characters = string.ascii_letters + string.digits  # letters and digits
    password = ''.join(random.choice(characters) for _ in range(length))
    return password


async def validate_user(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        db_user = await users_crud.get_user_by_username(db=db, username=user.username)
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    if not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    return db_user


async def update_password(user: UserOut, new_pass: str, db: Session = Depends(get_db)):
    try:
        db_user = await users_crud.get_user_by_username(db=db, username=user.username)
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    hashed_password = get_password_hash(new_pass)
    return await users_crud.update_user_password(db=db, username=user.username, password=hashed_password)
    