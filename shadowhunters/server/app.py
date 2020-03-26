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
        return {"error" : str(err)}, 404

    game.remove_player(player_id)
    games.update(game.dict(), where('uuid') == game_id)

    return {}

#
# /games/{game_id}/players/{player_id}/{action}
#
@app.post("/games/{game_id}/players/{player_id}/roll")
def player_interact_roll(game_id: str, player_id: str):
    """
    Given player tried to roll the dice
    """
    try:
        game = Game(**games.get(where('uuid') == game_id))
        game.roll(player_id)
    except Exception as err:
        return {"error" : str(err)}, 404

    games.update(game.dict(), where('uuid') == game_id)

    return {}

@app.post("/games/{game_id}/players/{player_id}/roll_target")
def player_interact_roll_target(game_id: str, player_id: str, location: Location):
    """
    Given player chooses which location they want to go to
    """
    try:
        game = Game(**games.get(where('uuid') == game_id))
        game.roll_target(player_id, location)
    except Exception as err:
        return {"error" : str(err)}, 404

    games.update(game.dict(), where('uuid') == game_id)

    return {}

@app.post("/games/{game_id}/players/{player_id}/action")
def player_interact_action(game_id: str, player_id: str):
    """
    Given player draws or activates ability on current tile
    """
    try:
        game = Game(**games.get(where('uuid') == game_id))
        game.action(player_id)
    except Exception as err:
        return {"error" : str(err)}, 404

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
    try:
        return games.get(where('uuid') == game_id)
    except Exception as e:
        print(repr(e))
        exit(1)

@app.delete("/games/{game_id}")
def delete_game(game_id : str):
    """
    Delete a game!
    """
    games.remove(where('uuid') == game_id)
    return {}