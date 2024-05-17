from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
import asyncio
import json
import random

from src.db.crud import gamestates_crud
from src.db.crud import leaderboard_crud
from src.db.crud import users_crud
from src.db.crud import game_crud

from ..db.schemas.users import UserOut
from ..db.database import SessionLocal
from src.auth.jwthandler import (
    get_current_user,
)

router = APIRouter()

json_file_path = "/app/src/assets/pictures.json"
with open (json_file_path, "r") as pictures_file: 
   pictures_object = json.load(pictures_file)

class Room:
  def __init__(self, room_id):
    self.room = room_id
    self.connections = {}
    self.timer_running = False

  async def broadcast(self, message, username):
    message["player_id"] = username
    for connection in self.connections.values():
        await connection.send_json(message)


  async def send_start_game(self, db):
     message = {}
     message["type"] = "start_game"
     await self.broadcast({"msg":"Game started.", "type":"message"}, "Server")
     for connection in self.connections.values():
        await connection.send_json(message)
      
     await self.send_start_round(db)

     await self.send_timer(db, 5, "timer_round_start")


  async def send_start_round(self, db):
     message = {}
     used_pictures_list = await game_crud.get_pictures_by_id(db=db, game_id=int(self.room))
     current_picture = get_new_random_picture_key(used_pictures_list)
     message["type"] = "start_round"
     message["picture"] = pictures_object.get(current_picture)
     current_correct = current_picture[:2]
     await game_crud.update_game_correct_current_guess(db, self.room, current_correct)
     await game_crud.update_game_pictures(db=db, game_id=self.room, new_picture=current_picture)
     await self.broadcast({"msg":"Round started.", "type":"message"}, "Server")
     for connection in self.connections.values():
        await connection.send_json(message)


  async def send_user_guessed(self, data, db, username):
    # Set this user to guessed and what guess was
    await gamestates_crud.update_game_state_has_guessed(db=db, game_id=self.room, player_id=data["player_id"], guessed=True, guess=data["current_guess"])
    await self.broadcast({"msg":"I have guessed.", "type":"has_guessed"}, username)
    # List of all alive game states
    # Check if all alive users have guessed
    count_guesses = 0
    game_states = await gamestates_crud.get_game_states(db=db, game_id=self.room)
    alive_game_states = []
    for game_state in game_states:
       if game_state.is_alive:
          alive_game_states.append(game_state)
          if game_state.has_guessed:
            count_guesses += 1
    
       
    # if so - End round
    if count_guesses == len(alive_game_states):
       self.timer_running = False
       await self.send_round_end(alive_users=alive_game_states, data=data, db=db)
    # else send timer to all users
    elif count_guesses == 1:
       self.timer_running = True
       await self.send_timer(db, 10, "timer_has_guessed")
       #await self.send_round_end(alive_users=alive_game_states, data=data, db=db)
    else:
       return

  
  async def send_round_end(self, alive_users, data, db):
     await asyncio.sleep(0.2)
     game = await game_crud.get_game_by_id(db=db, game_id=self.room)
     message = {}
     message["type"] = "round_end"
     message["correct_guess"] = game.correct_current_guess
     for connection in self.connections.values():
      await connection.send_json(message)

     # Check player guesses
     for alive_user in alive_users[:]:
        # if correct update score reset has_guessed and current_guess
        if alive_user.current_guess == game.correct_current_guess:
           await gamestates_crud.update_game_state_score(db=db, game_id=self.room, player_id=alive_user.player_id)
        # else kill player "type":"killed" and update bool to dead
        else:
            await gamestates_crud.update_game_state_alive(db=db, game_id=self.room, player_id=alive_user.player_id)
            alive_users.remove(alive_user)
            message = {}
            message["type"] = "killed"
            connection = self.connections[alive_user.player_id]
            await connection.send_json(message)

     # Update current correct guess to "" MIGHT BE REDUNTANT AS WE INSTANTLY UPDATE THESE VALUES IN START ROUND
     await game_crud.update_game_correct_current_guess(db=db, game_id=self.room, current_correct="")
     
     
     # Get scores of all users
     game_states = await gamestates_crud.get_game_states(db=db, game_id=self.room)
     user_scores = {}
     for game_state in game_states:
        user = await users_crud.get_user_by_id(db=db, id=game_state.player_id)
        username = user.username
        user_scores[username] = game_state.score

     message = {}
     #message["scores"] = user_scores

     # Check if any player alive
     if alive_users:
        # Send scores to all users
        message["type"] = "round_over"
        for connection in self.connections.values():
            await connection.send_json(message)

        await self.send_start_round(db=db)
        await asyncio.sleep(0.2)

        for game_state in game_states:
           await gamestates_crud.reset_game_state_guesses(db=db, game_id=self.room, player_id=game_state.player_id)

        message["type"] = "update_object"
        for connection in self.connections.values():
            await connection.send_json(message)

        await self.send_timer(db, 5, "timer_round_over")
        
     else:
        # Else Enter all states to leaderboard  and send "type":"game_over" to all players     
        message["type"] = "game_over"
        for connection in self.connections.values():
            await connection.send_json(message)
        # Update leaderboard (db) with user results
        for key, value in user_scores.items():
            await leaderboard_crud.create_leaderboard_entry(db=db, username=key, score=value)
  
  async def send_restart_game(self, db):
   await gamestates_crud.reset_game_states(db=db, game_id=self.room)
   message = {}
   message["type"] = "restart_game"
   for connection in self.connections.values():
            await connection.send_json(message)


  async def send_timer(self, db, time, type):
   message = {}
   for i in range(time, -1, -1):
      message["type"] = type
      message["timer"] = i
      for connection in self.connections.values():
            await connection.send_json(message)
      await asyncio.sleep(1)
      if not self.timer_running and type == "timer_has_guessed":
         return
      
   if(type == "timer_has_guessed"):
      await self.send_times_up()
      await asyncio.sleep(0.1)
   return
      
   
  async def send_times_up(self):
   message = {}
   message["type"] = "times_up"
   for connection in self.connections.values():
            await connection.send_json(message)
   return 


room_dict = {}


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_new_random_picture_key(used_keys):
   all_keys = set(pictures_object.keys())
   unused_keys = all_keys - set(used_keys)
   if unused_keys:
      new_random_key = random.choice(list(unused_keys))
      return new_random_key
   return None
 

@router.websocket('/ws/{room_id}/{client_id}')
async def websocket_endpoint(websocket:WebSocket, room_id: str, client_id: str, db: Session = Depends(get_db)):
    user = await users_crud.get_user_by_id(db=db, id=client_id)
    username = user.username
    room_id = int(room_id)

    try:
        await websocket.accept()
        if room_id not in room_dict:
            room_dict[room_id] = Room(room_id)
            await game_crud.create_game(db=db, game_id=room_id)
            room  = room_dict[room_id]
            room.connections[int(client_id)] = websocket
            await gamestates_crud.create_game_state(db=db, game_id=room_id, player_id=int(client_id), username=username, is_room_leader = True)
        else:
            room  = room_dict[room_id]
            room.connections[int(client_id)] = websocket
            await gamestates_crud.create_game_state(db=db, game_id=room_id, player_id=int(client_id), username=username)

        await room.broadcast({"msg":"Connected to the lobby", "type":"connected"}, username) # Creates a log in browser that a user joined

        while True:
            data = await websocket.receive_json()
            if data["type"] == "message":
                await room.broadcast(data, username)
            elif data["type"] == "start_game":
               await room.send_start_game(db)
            elif data["type"] == "user_guessed":
               await room.send_user_guessed(data, db, username)
            elif data["type"] == "restart_game":
               await room.send_restart_game(db)
            else:
               return "Tjelo :)"
    except WebSocketDisconnect:
        if room_id in room_dict:
            room = room_dict[room_id]

            disconnected_websocket = websocket

            userid_to_remove = None
            for userid, socket in room.connections.items():
                if socket == disconnected_websocket:
                    userid_to_remove = userid
                    break

            if userid_to_remove is not None:
                del room.connections[userid_to_remove]
                await game_crud.delete_game_state(db=db, room_id=room_id, player_id=userid_to_remove)

            if len(room.connections) == 0:
                del room_dict[room_id]
                await game_crud.delete_game(db=db, game_id=int(room_id))


@router.get("/sockets/lobbyID")
async def get_new_lobbyID(current_user: UserOut = Depends(get_current_user)):
    while True:
        rand_int = random.randint(1000, 9999)
        if rand_int not in room_dict:
            return rand_int
        

@router.get("/sockets/verify_lobbyID")
async def get_verify_lobbyID(lobby_id: int, current_user: UserOut = Depends(get_current_user)):
   if lobby_id in room_dict:
      return {"exists": True, "message": f"Lobby ID {lobby_id} exists."}
   else:
      return {"exists": False, "message": f"Lobby ID {lobby_id} does not exist."}
   

@router.get("/sockets/get_game_states_data")
async def get_game_states_data(lobby_id: int, current_user: UserOut = Depends(get_current_user), db: Session = Depends(get_db)):
   return await gamestates_crud.get_game_states_data(db=db, game_id=lobby_id)
   

@router.get("/sockets/get_game_states_data_end_of_round")
async def get_game_states_data(lobby_id: int, current_user: UserOut = Depends(get_current_user), db: Session = Depends(get_db)):
   return await gamestates_crud.get_game_states_data_end_of_round(db=db, game_id=lobby_id)
