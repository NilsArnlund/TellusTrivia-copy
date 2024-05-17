from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import and_

from .. import models
from src.db.schemas.game import GameStateOut

# Create GameState
async def create_game_state(db: Session, game_id: int, player_id: int, username: str, is_room_leader: bool  = False) -> GameStateOut:
    existing_game_state = db.query(models.GameState).filter(
        models.GameState.player_id == player_id
    ).first()
    
    if existing_game_state:

        db.delete(existing_game_state)
        db.commit() 

    new_game_state = models.GameState(
        game_id = game_id,
        player_id = player_id,
        is_alive = True,
        has_guessed = False,
        current_guess = "",
        score = 0,
        username = username,
        is_room_leader = is_room_leader
    )

    db.add(new_game_state)
    try:
        db.commit()
        db.refresh(new_game_state)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=401, detail=f"Sorry, Game ID: {new_game_state.game_id} for player ID: {new_game_state.player_id} already exists")
    return GameStateOut.from_orm(new_game_state)
    

# Get Game_state
async def get_game_state(db: Session, game_id: int, player_id: int):
    return db.query(models.GameState).filter(and_(
            models.GameState.game_id == game_id,
            models.GameState.player_id == player_id
        )).first() 


# Get Game_states
async def get_game_states(db: Session, game_id: int):
    return db.query(models.GameState).filter(models.GameState.game_id == game_id).all()


# Get states for users list component
async def get_game_states_data(db: Session, game_id: int):
    game_states = db.query(models.GameState).filter(models.GameState.game_id == game_id).with_entities(
        models.GameState.player_id,
        models.GameState.username,
        models.GameState.score,
        models.GameState.is_alive,
        models.GameState.is_room_leader,
        models.GameState.has_guessed
    ).all()
    
    structured_data = {}
    
    # Iterate through the list of game state data
    for index, state in enumerate(game_states, start=1):
        # Construct a dictionary for each state
        state_dict = {
            'username': state.username,
            'score': state.score,
            'is_alive': state.is_alive,
            'is_room_leader': state.is_room_leader,
            'has_guessed': state.has_guessed
        }
        
        structured_data[state.player_id] = state_dict
        
    return structured_data


# Get game states for end of round component
async def get_game_states_data_end_of_round(db: Session, game_id: int):
    game_states = db.query(models.GameState).filter(models.GameState.game_id == game_id).with_entities(
        models.GameState.player_id,
        models.GameState.username,
        models.GameState.score,
        models.GameState.is_alive,
        models.GameState.current_guess
    ).all()
    
    structured_data = {}
    
    # Iterate through the list of game state data
    for index, state in enumerate(game_states, start=1):
        # Construct a dictionary for each state
        state_dict = {
            'username': state.username,
            'score': state.score,
            'is_alive': state.is_alive,
            'current_guess': state.current_guess
        }
        structured_data[state.player_id] = state_dict
        
    return structured_data


# Delete GameState (Might be redundant as we remove every gamestate when removing a game)
async def delete_game_state(db:Session, room_id: int, player_id: int):
    existing_game_state = db.query(models.GameState).filter(
        models.GameState.game_id == room_id,
        models.GameState.player_id == player_id
    ).first()
    
    if existing_game_state:
        db.delete(existing_game_state)
        db.commit() 

# Update GameState (Alive)
async def update_game_state_alive(db: Session, game_id: int, player_id: int):
    game_state = db.query(models.GameState).filter(and_(
            models.GameState.game_id == game_id,
            models.GameState.player_id == player_id
        )).first() 

    if game_state:
        game_state.is_alive = False
        game_state.has_guessed = False
        
        try:
            db.commit()
            db.refresh(game_state)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"An error occurred while updating game_state alive: {e}")
    else:
        raise HTTPException(status_code=404, detail=f"Gamestate with game ID {game_id} and player ID {player_id} not found")
    return
    

# Update GameState (score)
async def update_game_state_score(db: Session, game_id: int, player_id: int):
    game_state = db.query(models.GameState).filter(and_(
            models.GameState.game_id == game_id,
            models.GameState.player_id == player_id
        )).first()   
    
    if game_state:
        game_state.score = game_state.score + 1
        
        try:
            db.commit()
            db.refresh(game_state)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"An error occurred while updating the game_state score: {e}")
    else:
        raise HTTPException(status_code=404, detail=f"Gamestate with game ID {game_id} and player ID {player_id} not found")
    return


# Reset GameState guesses
async def reset_game_state_guesses(db: Session, game_id: int, player_id: int):
    game_state = db.query(models.GameState).filter(and_(
            models.GameState.game_id == game_id,
            models.GameState.player_id == player_id
        )).first()   
    
    if game_state:
        game_state.has_guessed = False
        game_state.current_guess = "" 
        
        try:
            db.commit()
            db.refresh(game_state)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"An error occurred while updating the game_state score: {e}")
    else:
        raise HTTPException(status_code=404, detail=f"Gamestate with game ID {game_id} and player ID {player_id} not found")
    return
    

# Update GameState (has_guessed)
async def update_game_state_has_guessed(db: Session, game_id: int, player_id: int, guessed: bool, guess: str):
    game_state = db.query(models.GameState).filter(and_(
        models.GameState.game_id == game_id,
        models.GameState.player_id == player_id
    )).first()    

    if game_state:
        game_state.has_guessed = guessed
        game_state.current_guess = guess
        
        try:
            db.commit()
            db.refresh(game_state)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"An error occurred while updating the game_state has_guessed: {e}")
    else:
        raise HTTPException(status_code=404, detail=f"Gamestate with game ID {game_id} and player ID {player_id} not found")
    return

async def reset_game_states(db: Session, game_id: int):
    game_states = db.query(models.GameState).filter(and_(
        models.GameState.game_id == game_id
    )).all()

    for game_state in game_states:
        game_state.score = 0
        game_state.is_alive = True
        game_state.has_guessed = False
        game_state.current_guess = ""
        db.add(game_state)
    db.commit()
    # and so on
    return 


