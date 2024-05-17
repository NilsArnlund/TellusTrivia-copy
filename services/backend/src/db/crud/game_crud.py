from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import and_

from .. import models

from src.db.schemas.game import GameOut

# Create Game
async def create_game(db: Session, game_id: int) -> GameOut:
    new_game = models.Game(
        game_id = game_id,
        pictures = "",
        correct_current_guess = ""
    )

    db.add(new_game)

    try:
        db.commit()
        db.refresh(new_game)

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=401, detail=f"Sorry, Game ID: {new_game.game_id} already exists")
    return GameOut.from_orm(new_game)
    

# Get game
async def get_game_by_id(db:Session, game_id: int):
    return db.query(models.Game).filter(models.Game.game_id == game_id).first()


# Get game pictures by game_id
async def get_pictures_by_id(db:Session, game_id: int):
    game = db.query(models.Game).filter(models.Game.game_id == game_id).first()
    pictures_str = game.pictures
    return pictures_str.split(',')


# Delete Game and the gamestates 
async def delete_game(db: Session, game_id: int):
    game = db.query(models.Game).filter(models.Game.game_id == game_id).first()

    if game:
        db.delete(game)
        try:
            db.commit()
            return 
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"An error occurred while deleting the game: {e}")
    else:
        raise HTTPException(status_code=404, detail=f"Game with ID {game_id} not found")


# Update Game (Pictures)
async def update_game_pictures(db: Session, game_id: int, new_picture: str):
    game = db.query(models.Game).filter(models.Game.game_id == game_id).first()

    if game:
        if game.pictures:
            game.pictures += f",{new_picture}"
        else:
            game.pictures = new_picture
        
        try:
            db.commit()
            db.refresh(game)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"An error occurred while modifying the pictures: {e}")
    else:
        raise HTTPException(status_code=404, detail=f"Game with ID {game_id} not found")
    return
    

async def update_game_correct_current_guess(db: Session, game_id: int, current_correct: str):
    game = db.query(models.Game).filter(models.Game.game_id == game_id).first()

    if game:
        game.correct_current_guess = current_correct

        try:
            db.commit()
            db.refresh(game)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"An error occurred while updating current correct guess: {e}")
    else:
        raise HTTPException(status_code=404, detail=f"Game with ID {game_id} not found")
    return
