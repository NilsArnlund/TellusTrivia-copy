import base64
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from datetime import timedelta
import shutil
import os
import smtplib
from email.message import EmailMessage

from ..db.crud import users_crud
from ..db.schemas.users import UserIn, UserOut
from src.auth.users import validate_user, update_password, generate_random_password
from ..db.database import SessionLocal
from src.auth.jwthandler import (
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_refresh_token,
    verify_refresh_token
)

IMAGE_DIR = "profile_pictures/"
os.makedirs(IMAGE_DIR, exist_ok=True)

router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/users/create_user", response_model=UserOut)
async def create_user(user: UserIn, db: Session = Depends(get_db)):
    return await users_crud.create_user(db=db, user=user)


@router.post("/users/sign_in")
async def sign_in(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    db_user = await validate_user(user=form_data, db=db)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.username}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"sub": db_user.username})

    access_token_cookie = f"Bearer {access_token}"
    refresh_token_cookie = f"Bearer {refresh_token}"

    content = {"message": "You've successfully logged in. Welcome back!"}
    response = JSONResponse(content=content)
    response.set_cookie(
        "Authorization",
        value=access_token_cookie,
        httponly=True,
        max_age=1800,
        expires=1800,
        samesite="Lax",
        secure=False,
    )
    response.set_cookie(
        "Refresh-Token",
        value=refresh_token_cookie,
        httponly=True,
        max_age=604800,  
        expires=604800, 
        samesite="Lax",
        secure=False,
    )

    return response


@router.get("/refresh", status_code=status.HTTP_200_OK)
def get_new_access_token(request: Request):

    cookies = request.cookies
    refresh_token = cookies['Refresh-Token']

    username = verify_refresh_token(refresh_token)
    new_access_token = create_access_token(data={"sub": username})
    access_token_cookie = f"Bearer {new_access_token}"

    content = {"message": "You've successfully logged in. Welcome back!"}
    response = JSONResponse(content=content)
    response.set_cookie(
        "Authorization",
        value=access_token_cookie,
        httponly=True,
        max_age=1800,
        expires=1800,
        samesite="Lax",
        secure=False,
    )
    return response


@router.get("/users/me", response_model=UserOut)
async def read_users_me(current_user: UserOut = Depends(get_current_user)):
    return current_user


@router.get("/users/{username}", response_model=UserOut)
async def read_users_me(username: str, current_user: UserOut = Depends(get_current_user), db: Session = Depends(get_db)):
    user = await users_crud.get_user_by_username(db=db, username=username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No user found for username: {username}"
        )
    
    return user


@router.post("/users/uploadProfilePicture")
async def upload_profile_picture(file: UploadFile = File(...), current_user: UserOut = Depends(get_current_user), db: Session = Depends(get_db)):

    file_path = os.path.join(IMAGE_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    await users_crud.update_user_profile_picture(db=db, username=current_user.username, filename=file.filename)

    return JSONResponse({"message": "Profile image uploaded successfully", "filename": file.filename})


@router.get("/users/getUserProfilePicture/{username}")
async def get_user_profile_picture(username: str, current_user: UserOut = Depends(get_current_user), db: Session = Depends(get_db)):
    profile_picture_str = await users_crud.get_user_profile_picture(db=db, username=username)

    if not profile_picture_str:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No user found for username: {username}"
        )
    
    img_path = IMAGE_DIR + profile_picture_str
    with open(img_path, 'rb') as f:
        base64image = base64.b64encode(f.read())
    return base64image


@router.get("/users/getProfilePicture/me")
async def get_profile_picture_me(current_user: UserOut = Depends(get_current_user), db: Session = Depends(get_db)):
    profile_picture_str = await users_crud.get_user_profile_picture(db=db, username=current_user.username)

    if not profile_picture_str:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No user found for username: {current_user.username}"
        )
    
    img_path = IMAGE_DIR + profile_picture_str
    with open(img_path, 'rb') as f:
        base64image = base64.b64encode(f.read())
    return base64image


@router.put("/users/changePassword")
async def change_password(current_user: UserOut = Depends(get_current_user), new_pass: str = "", db: Session = Depends(get_db)):
    return await update_password(user=current_user, new_pass=new_pass, db=db)


@router.put("/users/resetPassword")
async def reset_password(email: str, db: Session = Depends(get_db)):
    user = await users_crud.get_user_by_email(db=db, email=email)
    if not user: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No user found for email: {email}"
        )
    new_password = generate_random_password()
    await update_password(user=user, new_pass=new_password, db=db)
    if new_password:
        sender = "mrhighexecutivetddd97@gmail.com"
        senderPassword = "xkmtdwnxculwqngi"
        
        mail = EmailMessage()
        mail['From'] = sender
        mail['To'] = email
        mail['Subject'] = "Twidder password reset"
        mail.set_content(f"Here is your new TerraTrivia password: {new_password}")
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(sender, senderPassword)
            server.sendmail(sender, email, mail.as_string())
            server.close()
            return 
        except Exception as exception:
            raise HTTPException(
            status_code=500,
            detail=f"There was a problem sending a new password"
        )
    else:
        raise HTTPException(
            status_code=500,
            detail=f"There was a problem creating a new password"
        )







     