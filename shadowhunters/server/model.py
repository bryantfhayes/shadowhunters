import json
import random

from tinydb import TinyDB, Query, where
from uuid import uuid4
from pydantic import BaseModel
from typing import List
from enum import Enum

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

class Team(str, Enum):
    Shadow = "shadow"
    Hunter = "hunter"
    Neutral = "neutral"
    Unassigned = "unassigned"

class DeckType(str, Enum):
    White = "white"
    Black = "black"
    Hermit = "hermit"

class Phase(str, Enum):
    Lobby = "lobby"
    Roll = "roll"

class Deck(BaseModel):
    cardtype: DeckType
    drawpile: List[int]
    discardpile: List[int]

    @classmethod
    def new_deck(cls, cardtype):
        drawpile = list(range(0, len(cards[cardtype.value])))
        random.shuffle(drawpile)
        return Deck(cardtype=cardtype, drawpile=drawpile, discardpile=[])

class Location(BaseModel):
    name : str
    description : str
    rolls : List[int]
    action : str

class Equipment(BaseModel):
    name : str
    description : str
    effect : str

class Role(BaseModel):
    name : str
    team : Team
    description : str
    ability : str
    maxhp : int
    damage : int

class Player(BaseModel):
    name : str
    uuid : str
    role : Role
    equipment : List[Equipment]
    location : Location

class Game(BaseModel):
    uuid : str
    players : List[Player]
    turn : int
    phase : Phase
    locations : List[Location]
    whitedeck : Deck
    blackdeck : Deck
    hermitdeck : Deck

    def new_player(self, name):
        default_role = Role(name="", team=Team.Unassigned, description="", ability="", maxhp=0, damage=0)
        default_location = Location(name="", description="", rolls=[], action="")
        player = Player(uuid=str(uuid4()), name=name, role=default_role, equipment=[], location=default_location)
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
        self.phase = Phase.Roll

        return True, ""

    @classmethod
    def new_game(cls):
        tiles = all_locations.copy()
        random.shuffle(tiles)
        locations = [Location(**t) for t in tiles]

        return cls(uuid=str(uuid4()), players=[], turn=-1, phase=Phase.Lobby, locations=locations, whitedeck=Deck.new_deck(DeckType.White), blackdeck=Deck.new_deck(DeckType.Black), hermitdeck=Deck.new_deck(DeckType.Hermit))
