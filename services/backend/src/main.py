from fastapi import Depends, FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .db import models, schemas
from .db.database import SessionLocal, engine
from .routers import users, sockets, leaderboard

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(sockets.router)
app.include_router(leaderboard.router)


@app.get("/hello")
async def root():
    return{"message": "Hello world"}




