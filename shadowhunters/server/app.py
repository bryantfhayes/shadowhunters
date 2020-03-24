import json
import random

from fastapi import FastAPI
from tinydb import Query, where
from uuid import uuid4
from model import db, games
from model import Game, Role, Equipment, Location, Deck, Player
from model import MAX_PLAYER_COUNT

app = FastAPI()

#
# /games/{id}/start
#
@app.post("/games/{game_id}/start")
def start_game(game_id):
    """
    Start game!
    """
    try:
        game = Game(**games.get(where('uuid') == game_id))
    except Exception as err:
        return {"error" : err}, 404
    
    status, error = game.start()
    if status is False:
        return {"error" : error}, 400

    games.update(game.dict(), where('uuid') == game_id)

    return {}

#
# /games/{id}/players
#

@app.get("/games/{game_id}/players")
def get_players(game_id):
    try:
        game = Game(**games.get(where('uuid') == game_id))
    except Exception as err:
        return {"error" : err}, 404

    return game.players.dict()

@app.post("/games/{game_id}/players")
def new_player(game_id, name: str):
    """
    Make a new player in a game!
    """
    try:
        game = Game(**games.get(where('uuid') == game_id))
    except Exception as err:
        return {"error" : err}, 404
    
    if len(game.players) >= MAX_PLAYER_COUNT:
        return {"error" : "The game is full"}, 404

    player = game.new_player(name)

    games.update(game.dict(), where('uuid') == game_id)

    return player.dict()

@app.delete("/games/{game_id}/players/{player_id}")
def delete_player(game_id, player_id):
    """
    Delete a player from a game!
    """
    try:
        game = Game(**games.get(where('uuid') == game_id))
    except Exception as err:
        return {"error" : err}, 404

    game.remove_player(player_id)
    games.update(game.dict(), where('uuid') == game_id)

    return {}

#
# /games
#

@app.get("/games")
def get_games():
    return games.all()

@app.post("/games")
def new_game():
    """
    Make a new game!
    """
    game = Game.new_game()
    games.insert(game.dict())
    return game

@app.get("/games/{game_id}")
def get_game(game_id : str):
    return games.get(where('uuid') == game_id)

@app.delete("/games/{game_id}")
def delete_game(game_id : str):
    """
    Delete a game!
    """
    games.remove(where('uuid') == game_id)
    return {}