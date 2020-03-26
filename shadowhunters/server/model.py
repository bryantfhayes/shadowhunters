import json
import random

from tinydb import TinyDB, Query, where
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware

from uuid import uuid4
from pydantic import BaseModel
from typing import List, Dict
from enum import Enum

db = TinyDB('db.json', storage=CachingMiddleware(JSONStorage))
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

#
# Helpers
#
def get_uuid():
    """
    Get a unique identifier
    """
    return str(uuid4())

#
# Models
#

class Team(str, Enum):
    Shadow = "shadow"
    Hunter = "hunter"
    Neutral = "neutral"
    Unassigned = "unassigned"

class LocationAction(str, Enum):
    DrawHermit = "draw_hermit"
    DrawBlack = "draw_black"
    DrawWhite = "draw_white"
    DrawAny = "draw_any"
    StealEquipment = "steal_equipment"
    WeirdWoods = "weird_woods"
    Unassigned = "unassigned"

class DeckType(str, Enum):
    White = "white"
    Black = "black"
    Hermit = "hermit"
    Unassigned = "unassigned"

class Card(BaseModel):
    index: int
    name: str
    type: DeckType
    description: str
    effect: str

class Phase(str, Enum):
    Lobby = "lobby"
    Roll = "roll"
    RollTarget = "roll_target"
    Action = "action"
    ActionTarget = "action_target"
    ActionResponse = "action_response"
    Attack = "attack"
    AttackTarget = "attack_target"
    AttackResponse = "attack_response"
    ActionChoice = "action_choice"

class Deck(BaseModel):
    cardtype: DeckType
    drawpile: List[int]
    discardpile: List[int]

    @classmethod
    def new_deck(cls, cardtype):
        drawpile = list(range(0, len(cards[cardtype.value])))
        random.shuffle(drawpile)
        return Deck(cardtype=cardtype, drawpile=drawpile, discardpile=[])

    def draw(self):
        """
        Draw a card from the deck, and return actual card data
        """
        picked = self.drawpile.pop(0)
        self.discardpile.append(picked)
        return Card(**cards[self.cardtype.value][picked])

class Location(BaseModel):
    name : str
    description : str
    rolls : List[int]
    action : LocationAction

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

class ActionResult(BaseModel):
    location_action: LocationAction
    card: Card

class Game(BaseModel):
    uuid : str
    players : Dict[str, Player]
    turn : str
    turn_index : int
    phase : Phase
    last_roll : int
    notifications : List[str]
    locations : List[Location]
    turn_order : List[str]
    whitedeck : Deck
    blackdeck : Deck
    hermitdeck : Deck
    action_results = ActionResult(location_action=LocationAction.Unassigned, card=Card(index=-1, name="", type=DeckType.Unassigned, description="", effect=""))

    def notify(self, msg):
        self.notifications.append(msg)
        print(msg)

    def rolldice(self, d4=True, d6=True):
        """
        Roll a X-sided dice
        """
        if d4 and d6:
            return random.randint(2, 10)
        elif d4:
            return random.randint(1, 4)
        elif d6:
            return random.randint(1, 6)
        else:
            raise RuntimeError("Bad dice combo!")

    def new_player(self, name):
        default_role = Role(name="", team=Team.Unassigned, description="", ability="", maxhp=0, damage=0)
        default_location = Location(name="", description="", rolls=[], action=LocationAction.Unassigned)
        player = Player(uuid=get_uuid(), name=name, role=default_role, equipment=[], location=default_location)
        self.players[player.uuid] = player
        return player

    def advance_turn(self):
        self.turn_index += 1
        if self.turn_index >= len(self.turn_order):
            self.turn_index = 0
        self.turn = self.turn_order[self.turn_index]

    def roll(self, player_id):
        """
        Perform a roll operation for a designated player
        """
        if player_id not in self.players:
            raise RuntimeError("Invalid player!")
        
        if player_id != self.turn:
            raise RuntimeError("Not your turn!")

        if self.phase != Phase.Roll:
            raise RuntimeError("You can't do that right now!")

        self.last_roll = self.rolldice(d4=True, d6=True)
        self.notify("{0} rolled a {1}!".format(self.players[player_id].name, self.last_roll))

        if self.last_roll == 7:
            self.notify("{0} is choosing where they want to move!".format(self.players[player_id].name))
            self.phase = Phase.RollTarget
        else:
            new_location = None
            for location in self.locations:
                if self.last_roll in location.rolls:
                    new_location = location
                    break
            self.players[player_id].location = new_location
            self.notify("{0} moved to {1}!".format(self.players[player_id].name, self.players[player_id].location.name))

            self.phase = Phase.Action

    def roll_target(self, player_id, location):
        """
        Perform a roll_target operation for a designated player
        """
        if player_id not in self.players:
            raise RuntimeError("Invalid player!")
        
        if player_id != self.turn:
            raise RuntimeError("Not your turn!")

        if self.phase != Phase.RollTarget:
            raise RuntimeError("You can't do that right now!")

        self.players[player_id].location = location
        self.notify("{0} moved to {1}!".format(self.players[player_id].name, self.players[player_id].location.name))

        self.phase = Phase.Action

    def action(self, player_id):
        """
        Perform a location-based action operation for a designated player
        """
        if player_id not in self.players:
            raise RuntimeError("Invalid player!")
        
        if player_id != self.turn:
            raise RuntimeError("Not your turn!")

        if self.phase != Phase.Action:
            raise RuntimeError("You can't do that right now!")

        # Draw a card or activate location ability
        location = self.players[player_id].location
        if location.action == LocationAction.DrawBlack:
            self.notify("{0} drew a black card!".format(self.players[player_id].name))
            blackcard = self.game.blackdeck.draw()
            self.action_results = ActionResult(location.action, blackcard)
        elif location.action == LocationAction.DrawHermit:
            self.notify("{0} drew a hermit card!".format(self.players[player_id].name))
            hermitcard = self.game.hermitdeck.draw()
            self.action_results = ActionResult(location.action, hermitcard)
        elif location.action == LocationAction.DrawWhite:
            self.notify("{0} drew a white card!".format(self.players[player_id].name))
            whitecard = self.game.whitedeck.draw()
            self.action_results = ActionResult(location.action, whitecard)
        elif location.action == LocationAction.StealEquipment:
            self.notify("{0} chose to steam an equipment!".format(self.players[player_id].name))
            self.phase = Phase.ActionChoice
            self.action_results.location_action = location.action
        elif location.action == LocationAction.WeirdWoods:
            self.notify("{0} activated the weird woods!".format(self.players[player_id].name))
            self.phase = Phase.ActionChoice
            self.action_results.location_action = location.action
        elif location.action == LocationAction.DrawAny:
            self.notify("{0} is choosing a card to draw!".format(self.players[player_id].name))
            self.phase = Phase.ActionChoice
            self.action_results.location_action = location.action
        else:
            raise RuntimeError("Not a valid location!")

        self.phase = Phase.ActionTarget

    def remove_player(self, player_id):
        if player_id in self.players:
            del self.players[player_id]

    def start(self):
        if len(self.players.keys()) not in roles_for_player_count:
            return False, "Not enough players!"

        # Make a list of potential roles in this game
        possible_roles = []
        all_roles = list(roles)
        for role in roles_for_player_count[len(self.players.keys())]:
            # Pick a role from the list
            selected_role = random.choice([r for r in all_roles if r["team"] == role])
            possible_roles.append(selected_role)

            # Whichever you picked, remove it from the available lsit of roles
            all_roles = [r for r in all_roles if r["name"] != selected_role["name"]]

        # Assign roles to all players
        for _, player in self.players.items():
            # Pick a role from the chosen list for this game
            selected_role = random.choice(possible_roles)
            player.role = Role(**selected_role)

            # Whichever you picked, remove it from the available lsit of roles
            possible_roles = [r for r in possible_roles if r["name"] != selected_role["name"]]

        # Get turn order
        self.turn_order = list(self.players.keys())
        random.shuffle(self.turn_order)

        # Set game to player 0's turn
        self.turn = self.turn_order[0]
        self.phase = Phase.Roll

        return True, ""

    @classmethod
    def new_game(cls):
        tiles = all_locations.copy()
        random.shuffle(tiles)
        locations = [Location(**t) for t in tiles]

        return cls(uuid=get_uuid(), players={}, turn="", turn_index=0, phase=Phase.Lobby, last_roll=0, notifications=[], locations=locations, turn_order=[], whitedeck=Deck.new_deck(DeckType.White), blackdeck=Deck.new_deck(DeckType.Black), hermitdeck=Deck.new_deck(DeckType.Hermit))
