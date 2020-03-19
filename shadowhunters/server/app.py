from fastapi import FastAPI
from tinydb import TinyDB, Query, where
from uuid import uuid4
from marshmallow import Schema, fields, pprint, post_load, ValidationError
import json
import random

app = FastAPI()
db = TinyDB('db.json')
games = db.table("games")

MAX_PLAYER_COUNT = 8

roles = [
    {"name" : "role-1", "team" : "shadow", "description" : "this is a description", "ability" : "This is an ability", "maxhp" : 10, "damage" : 0},
    {"name" : "role-2", "team" : "shadow", "description" : "this is a description", "ability" : "This is an ability", "maxhp" : 10, "damage" : 0},
    {"name" : "role-3", "team" : "shadow", "description" : "this is a description", "ability" : "This is an ability", "maxhp" : 10, "damage" : 0},
    {"name" : "role-4", "team" : "shadow", "description" : "this is a description", "ability" : "This is an ability", "maxhp" : 10, "damage" : 0},
    {"name" : "role-5", "team" : "hunter", "description" : "this is a description", "ability" : "This is an ability", "maxhp" : 10, "damage" : 0},
    {"name" : "role-6", "team" : "hunter", "description" : "this is a description", "ability" : "This is an ability", "maxhp" : 10, "damage" : 0},
    {"name" : "role-7", "team" : "hunter", "description" : "this is a description", "ability" : "This is an ability", "maxhp" : 10, "damage" : 0},
    {"name" : "role-8", "team" : "hunter", "description" : "this is a description", "ability" : "This is an ability", "maxhp" : 10, "damage" : 0},
    {"name" : "role-9", "team" : "neutral", "description" : "this is a description", "ability" : "This is an ability", "maxhp" : 10, "damage" : 0},
    {"name" : "role-10", "team" : "neutral", "description" : "this is a description", "ability" : "This is an ability", "maxhp" : 10, "damage" : 0},
    {"name" : "role-11", "team" : "neutral", "description" : "this is a description", "ability" : "This is an ability", "maxhp" : 10, "damage" : 0},
    {"name" : "role-12", "team" : "neutral", "description" : "this is a description", "ability" : "This is an ability", "maxhp" : 10, "damage" : 0}
]

roles_for_player_count = {
    3 : ["shadow", "hunter", "neutral"],
    4 : ["shadow", "hunter", "neutral", "neutral"],
    5 : ["shadow", "hunter", "shadow", "hunter", "neutral"],
    6 : ["shadow", "hunter", "shadow", "hunter", "neutral", "neutral"],
    7 : ["shadow", "hunter", "shadow", "hunter", "shadow", "hunter", "neutral"],
    8 : ["shadow", "hunter", "shadow", "hunter", "shadow", "hunter", "neutral", "neutral"]
}

all_locations = [
    {"name" : "Hermit's Cabin", "rolls" : [2, 3], "description" : "You may draw a Hermit card", "action" : "draw_hermit"},
    {"name" : "Underworld Gate", "rolls" : [4, 5], "description" : "You may draw a card from the stack of your choice", "action" : "draw_any"},
    {"name" : "Church", "rolls" : [6], "description" : "You may draw a White card", "action" : "draw_white"},
    {"name" : "Cemetery", "rolls" : [8], "description" : "You may draw a Black card", "action" : "draw_black"},
    {"name" : "Weird Woods", "rolls" : [9], "description" : "You may either give 2 damage to any player or heal 1 damage of any player", "action" : "weird_woods"},
    {"name" : "Erstwhile Altar", "rolls" : [10], "description" : "You may steal an Equipment card from any player", "action" : "steal_equipment"}
]

cards = {
    "white" : [
        {"index" : 0, "name" : "cardname", "type" : "white", "description" : "fsdfsdfsdf", "effect" : "do_something"},
        {"index" : 1, "name" : "cardname", "type" : "white", "description" : "fsdfsdfsdf", "effect" : "do_something"},
        {"index" : 2, "name" : "cardname", "type" : "white", "description" : "fsdfsdfsdf", "effect" : "do_something"},
        {"index" : 3, "name" : "cardname", "type" : "white", "description" : "fsdfsdfsdf", "effect" : "do_something"},
        {"index" : 4, "name" : "cardname", "type" : "white", "description" : "fsdfsdfsdf", "effect" : "do_something"},
        {"index" : 5, "name" : "cardname", "type" : "white", "description" : "fsdfsdfsdf", "effect" : "do_something"}
    ],
    "black" : [
        {"index" : 0, "name" : "cardname", "type" : "black", "description" : "fsdfsdfsdf", "effect" : "do_something"},
        {"index" : 1, "name" : "cardname", "type" : "black", "description" : "fsdfsdfsdf", "effect" : "do_something"},
        {"index" : 2, "name" : "cardname", "type" : "black", "description" : "fsdfsdfsdf", "effect" : "do_something"},
        {"index" : 3, "name" : "cardname", "type" : "black", "description" : "fsdfsdfsdf", "effect" : "do_something"},
        {"index" : 4, "name" : "cardname", "type" : "black", "description" : "fsdfsdfsdf", "effect" : "do_something"},
        {"index" : 5, "name" : "cardname", "type" : "black", "description" : "fsdfsdfsdf", "effect" : "do_something"}
    ],
    "hermit" : [
        {"index" : 0, "name" : "cardname", "type" : "hermit", "description" : "fsdfsdfsdf", "effect" : "do_something"},
        {"index" : 1, "name" : "cardname", "type" : "hermit", "description" : "fsdfsdfsdf", "effect" : "do_something"},
        {"index" : 2, "name" : "cardname", "type" : "hermit", "description" : "fsdfsdfsdf", "effect" : "do_something"},
        {"index" : 3, "name" : "cardname", "type" : "hermit", "description" : "fsdfsdfsdf", "effect" : "do_something"},
        {"index" : 4, "name" : "cardname", "type" : "hermit", "description" : "fsdfsdfsdf", "effect" : "do_something"},
        {"index" : 5, "name" : "cardname", "type" : "hermit", "description" : "fsdfsdfsdf", "effect" : "do_something"}
    ]
}


class Deck(object):
    def __init__(self, cardtype, drawpile, discardpile=[]):
        self.cardtype = cardtype
        self.drawpile = drawpile
        self.discardpile = discardpile

    @classmethod
    def new_deck(cls, decktype):
        drawpile = list(range(0, len(cards[decktype])))
        random.shuffle(drawpile)
        return Deck(decktype, drawpile, [])

class DeckSchema(Schema):
    cardtype = fields.Str()
    drawpile = fields.List(fields.Int())
    discardpile = fields.List(fields.Int())

class Location(object):
    def __init__(self, name, description, rolls, action):
        self.name = name
        self.rolls = rolls
        self.description = description
        self.action = action

class LocationSchema(Schema):
    name = fields.Str()
    description = fields.Str()
    rolls = fields.List(fields.Int())
    action = fields.Str()

    @post_load
    def make_location(self, data, **kwargs):
        return Location(**data)

class Equipment(object):
    def __init__(self, name, description, effect):
        self.name = name
        self.description = description
        self.effect = effect

class EquipmentSchema(Schema):
    name = fields.Str()
    description = fields.Str()
    effect = fields.Str()

    @post_load
    def make_equipment(self, data, **kwargs):
        return Equipment(**data)

class Role(object):
    def __init__(self, name="", team="", description="", ability="", maxhp=0, damage=0):
        self.name = name
        self.team = team
        self.description = description
        self.ability = ability
        self.maxhp = maxhp
        self.damage = damage

class RoleSchema(Schema):
    name = fields.Str()
    team = fields.Str()
    description = fields.Str()
    ability = fields.Str()
    maxhp = fields.Int()
    damage = fields.Int()

    @post_load
    def make_role(self, data, **kwargs):
        return Role(**data)

class Player(object):
    def __init__(self, uuid, name, role, equipment=[], location=None):
        self.uuid = uuid
        self.name = name
        self.role = role
        self.equipment = equipment
        self.location = location

class PlayerSchema(Schema):
    name = fields.Str()
    uuid = fields.Str()
    role = fields.Nested(RoleSchema())
    equipment = fields.Nested(EquipmentSchema(many=True))
    location = fields.Nested(LocationSchema())

    @post_load
    def make_player(self, data, **kwargs):
        return Player(**data)

class Game(object):
    def __init__(self, uuid, players=[], turn=0, phase="LOBBY", locations=[], whitedeck=None, blackdeck=None, hermitdeck=None):
        self.uuid = uuid
        self.players = players
        self.turn = turn
        self.phase = phase
        self.locations = locations
        self.whitedeck = whitedeck
        self.blackdeck = blackdeck
        self.hermitdeck = hermitdeck

    def new_player(self, name):
        player = Player(uuid=uuid4(), name=name, role=Role(), equipment=[], location=Location(name="", description="", rolls=[], action=""))
        self.players.append(player)
        return player

    def remove_player(self, player_id):
        for i, o in enumerate(self.players):
            if o.uuid == player_id:
                del self.players[i]
                break

    def start(self):
        if len(self.players) not in roles_for_player_count:
            return False, "Not enough players!"

        # Make a list of potential roles in this game
        possible_roles = []
        all_roles = list(roles)
        for role in roles_for_player_count[len(self.players)]:
            # Pick a role from the list
            selected_role = random.choice([r for r in all_roles if r["team"] == role])
            possible_roles.append(selected_role)

            # Whichever you picked, remove it from the available lsit of roles
            all_roles = [r for r in all_roles if r["name"] != selected_role["name"]]

        # Assign roles to all players
        for player in self.players:
            # Pick a role from the chosen list for this game
            selected_role = random.choice(possible_roles)
            player.role = Role(**selected_role)

            # Whichever you picked, remove it from the available lsit of roles
            possible_roles = [r for r in possible_roles if r["name"] != selected_role["name"]]

        # Set game to player 0's turn
        self.turn = 0
        self.phase = "ROLL"

        return True, ""

    @classmethod
    def new_game(cls):
        tiles = all_locations.copy()
        random.shuffle(tiles)
        locations = [Location(**t) for t in tiles]

        return cls(uuid4(), locations=locations, whitedeck=Deck.new_deck("white"), blackdeck=Deck.new_deck("black"), hermitdeck=Deck.new_deck("hermit"))

class GameSchema(Schema):
    uuid = fields.Str()
    players = fields.Nested(PlayerSchema(many=True))
    turn = fields.Int()
    phase = fields.Str()
    locations = fields.Nested(LocationSchema(many=True))
    whitedeck = fields.Nested(DeckSchema())
    blackdeck = fields.Nested(DeckSchema())
    hermitdeck = fields.Nested(DeckSchema())

    @post_load
    def make_game(self, data, **kwargs):
        return Game(**data)

#
# /games/{id}/start
#
@app.post("/games/{game_id}/start")
def start_game(game_id):
    """
    Start game!
    """
    schema = GameSchema()
    try:
        game = schema.load(games.get(where('uuid') == game_id))
    except ValidationError as err:
        return {"error" : err}, 404
    
    status, error = game.start()
    if status is False:
        return {"error" : error}, 400

    schema = GameSchema()
    games.update(schema.dump(game), where('uuid') == game_id)

    return {}


#
# /games/{id}/players
#

@app.get("/games/{game_id}/players")
def get_players(game_id):
    schema = GameSchema()
    try:
        game = schema.load(games.get(where('uuid') == game_id))
    except ValidationError as err:
        return {"error" : err}, 404

    schema = PlayerSchema()
    players = schema.dump(game.players, many=True)
    return players

@app.post("/games/{game_id}/players")
def new_player(game_id, name: str):
    """
    Make a new player in a game!
    """
    schema = GameSchema()
    try:
        game = schema.load(games.get(where('uuid') == game_id))
    except ValidationError as err:
        return {"error" : err}, 404
    
    if len(game.players) >= MAX_PLAYER_COUNT:
        return {"error" : "The game is full"}, 404

    player = game.new_player(name)

    schema = GameSchema()
    games.update(schema.dump(game), where('uuid') == game_id)

    schema = PlayerSchema()
    return schema.dump(player)

@app.delete("/games/{game_id}/players/{player_id}")
def delete_player(game_id, player_id):
    """
    Delete a player from a game!
    """
    schema = GameSchema()
    try:
        game = schema.load(games.get(where('uuid') == game_id))
    except ValidationError as err:
        return {"error" : err}, 404

    game.remove_player(player_id)
    games.update(schema.dump(game), where('uuid') == game_id)

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
    schema = GameSchema()
    game = Game.new_game()
    games.insert(schema.dump(game))
    return game

@app.get("/games/{game_id}")
def get_game(game_id):
    return games.get(where('uuid') == game_id)

@app.delete("/games/{game_id}")
def delete_game(game_id):
    """
    Delete a game!
    """
    games.remove(where('uuid') == game_id)
    return {}