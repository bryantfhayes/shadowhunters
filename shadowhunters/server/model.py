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
    Nothing = "nothing"

class ChoiceType(str, Enum):
    Movement = "movement" # Player chooses where to move their player
    Deck = "deck"         # Player chooses which deck to draw from
    Draw = "draw"         # Player chooses whether they draw card or not
    Steal = "steal"       # Player chooses whether or not to steal from someone
    StealTarget = "steal_target" # Player chooses which player to steal from
    WeirdWoods = "wierd_woods"   # Player chooses whether to use weird woods or not
    WeirdWoodsAbility = "weird_woods_ability" # Player chooses which ability to use
    WeirdWoodsTarget = "weird_woods_target" # Player chooses target for weird woods
    Nothing = "nothing"

class EffectType(str, Enum):
    Heal = "heal"
    Damage = "damage"
    Nothing = "nothing"

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
    ChoiceNeeded = "choice_needed"
    Idle = "idle"

class Deck(BaseModel):
    cardtype: DeckType
    drawpile: List[int]
    discardpile: List[int]

    @classmethod
    def new_deck(cls, cardtype):
        drawpile = list(range(0, len(cards[cardtype.value])))
        random.shuffle(drawpile)
        return cls(cardtype=cardtype, drawpile=drawpile, discardpile=[])

    def draw(self):
        """
        Draw a card from the deck, and return actual card data
        """
        if len(self.drawpile) == 0:
            return None
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

class Effect(BaseModel):
    type : EffectType
    val : int

class Player(BaseModel):
    name : str
    uuid : str
    role : Role
    equipment : List[Equipment]
    location : Location

class ActionResult(BaseModel):
    location_action: LocationAction
    card: Card

class Choice(BaseModel):
    type: ChoiceType
    prompt: str
    location_options: List[Location]
    player_options: List[Player]
    string_options: List[str]
    deck_options: List[DeckType]
    equipment_options: List[Equipment]

    @classmethod
    def new_movement_choice(cls, options):
        return cls(type=ChoiceType.Movement, prompt="Choose where you would like to move.", location_options=options, player_options=[], deck_options=[], string_options=[], equipment_options=[])
    
    @classmethod
    def new_deck_choice(cls):
        return cls(type=ChoiceType.Deck, prompt="Which deck would you like to draw from?", location_options=[], player_options=[], deck_options=[DeckType.Hermit, DeckType.Black, DeckType.White, DeckType.Nothing], string_options=[], equipment_options=[])

    @classmethod
    def new_draw_choice(cls, prompt):
        return cls(type=ChoiceType.Draw, prompt=prompt, location_options=[], player_options=[], deck_options=[], string_options=["yes", "no"], equipment_options=[])

    @classmethod
    def new_steal_choice(cls):
        return cls(type=ChoiceType.Steal, prompt="Do you want to steal an equipment card?", location_options=[], player_options=[], deck_options=[], string_options=["yes", "no"], equipment_options=[])

    @classmethod
    def new_steal_target_choice(cls, options):
        return cls(type=ChoiceType.StealTarget, prompt="Which equipment do you want to steal?", location_options=[], player_options=[], deck_options=[], string_options=[], equipment_options=options)
    
    @classmethod
    def new_weird_woods_choice(cls):
        return cls(type=ChoiceType.WeirdWoods, prompt="Do you want to use weird woods power?", location_options=[], player_options=[], deck_options=[], string_options=["yes", "no"], equipment_options=[])

    @classmethod
    def new_weird_woods_ability_choice(cls):
        return cls(type=ChoiceType.WeirdWoodsAbility, prompt="Do you want to heal someone or hurt someone?", location_options=[], player_options=[], deck_options=[], string_options=["heal", "hurt"], equipment_options=[])

    @classmethod
    def new_weird_woods_target_choice(cls, options):
        return cls(type=ChoiceType.WeirdWoodsTarget, prompt="Who do you want to target weird woods ability on?", location_options=[], player_options=options, deck_options=[], string_options=[], equipment_options=[])

    @classmethod
    def new_empty_choice(cls):
        return cls(type=ChoiceType.Nothing, prompt="", location_options=[], player_options=[], deck_options=[], string_options=[], equipment_options=[])

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
    current_choice : Choice
    loaded_effect : Effect

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
        self.phase = Phase.Roll
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
            self.current_choice = Choice.new_movement_choice(options=self.locations)
            self.phase = Phase.ChoiceNeeded
        else:
            new_location = None
            for location in self.locations:
                if self.last_roll in location.rolls:
                    new_location = location
                    break

            self.move_player(player_id, new_location)

    def move_player(self, player_id, location):
        self.notify("{0} moved to {1}!".format(self.players[player_id].name, location.name))
        self.players[player_id].location = location

        # Draw a card or activate location ability next
        if location.action == LocationAction.DrawBlack:
            self.current_choice = Choice.new_draw_choice("Would you like to draw a black card?")
        elif location.action == LocationAction.DrawHermit:
            self.current_choice = Choice.new_draw_choice("Would you like to draw a hermit card?")
        elif location.action == LocationAction.DrawWhite:
            self.current_choice = Choice.new_draw_choice("Would you like to draw a white card?")
        elif location.action == LocationAction.StealEquipment:
            self.current_choice = Choice.new_steal_choice()
        elif location.action == LocationAction.WeirdWoods:
            self.current_choice = Choice.new_weird_woods_choice()
        elif location.action == LocationAction.DrawAny:
            self.current_choice = Choice.new_deck_choice()
        else:
            raise RuntimeError("Not a valid location!")

        self.phase = Phase.ChoiceNeeded

    def make_choice(self, player_id, choice_idx):
        if player_id not in self.players:
            raise RuntimeError("Invalid player!")
        
        if player_id != self.turn:
            raise RuntimeError("Not your turn!")

        if self.phase != Phase.ChoiceNeeded:
            raise RuntimeError("You can't do that right now!")

        # Movement Selection

        if self.current_choice.type == ChoiceType.Movement:
            target_location = self.current_choice.location_options[choice_idx]
            self.move_player(player_id, target_location)

        # Choose Deck

        elif self.current_choice.type == ChoiceType.Deck:
            target_deck = self.current_choice.deck_options[choice_idx]
            if target_deck == DeckType.Nothing:
                self.phase = Phase.Idle
            else:
                self.draw_card(target_deck)
                self.phase = Phase.Idle

        # Choose Draw

        elif self.current_choice.type == ChoiceType.Draw:
            choice = self.current_choice.string_options[choice_idx]
            if choice == "yes":
                card = None
                if self.players[self.turn].location.action == LocationAction.DrawHermit:
                    card = self.draw_card(DeckType.Hermit)
                elif self.players[self.turn].location.action == LocationAction.DrawBlack:
                    card = self.draw_card(DeckType.Black)
                elif self.players[self.turn].location.action == LocationAction.DrawWhite:
                    card = self.draw_card(DeckType.White)
                print("E")
                self.phase = Phase.Idle
            else:
                self.phase = Phase.Idle

        # Steal Equipment

        elif self.current_choice.type == ChoiceType.Steal:
            choice = self.current_choice.string_options[choice_idx]
            if choice == "yes":
                available_equipment = []
                for uuid, player in self.players.items():
                    available_equipment.extend(player.equipment)
                if len(available_equipment) <= 0:
                    print("No equipment to steal")
                    self.phase = Phase.Idle
                else:
                    self.current_choice = Choice.new_steal_target_choice(available_equipment)
                    self.phase = Phase.ChoiceNeeded
            else:
                self.phase = Phase.Idle

        elif self.current_choice.type == ChoiceType.StealTarget:
            target_equipment = self.current_choice.equipment_options[choice_idx]

        # Weird Woods

        elif self.current_choice.type == ChoiceType.WeirdWoods:
            choice = self.current_choice.string_options[choice_idx]
            if choice == "yes":
                self.current_choice = Choice.new_weird_woods_ability_choice()
                self.phase = Phase.ChoiceNeeded
            else:
                self.phase = Phase.Idle

        elif self.current_choice.type == ChoiceType.WeirdWoodsAbility:
            choice = self.current_choice.string_options[choice_idx]
            if choice == "heal":
                self.loaded_effect = Effect(type=EffectType.Heal, val=1)
                self.current_choice = Choice.new_weird_woods_target_choice(list(self.players.values()))
                self.phase = Phase.ChoiceNeeded
            else:
                self.loaded_effect = Effect(type=EffectType.Damage, val=2)
                self.current_choice = Choice.new_weird_woods_target_choice(list(self.players.values()))
                self.phase = Phase.ChoiceNeeded

        elif self.current_choice.type == ChoiceType.WeirdWoodsTarget:
            target_player = self.current_choice.player_options[choice_idx]
            self.phase = Phase.Idle

    def draw_card(self, deck):
        card = None
        if deck == DeckType.Black:
            card = self.blackdeck.draw()
        elif deck == DeckType.White:
            card = self.whitedeck.draw()
        else:
            card = self.hermitdeck.draw()

        if card is None:
            self.notify("No more cards of that type to draw")
        else:
            self.notify("{0} drew a {1} card: {2}".format(self.players[self.turn].name, deck, card))
        
        return card

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
        default_choice = Choice.new_empty_choice()

        return cls(uuid=get_uuid(), players={}, turn="", turn_index=0, phase=Phase.Lobby, last_roll=0, notifications=[], locations=locations, turn_order=[], whitedeck=Deck.new_deck(DeckType.White), blackdeck=Deck.new_deck(DeckType.Black), hermitdeck=Deck.new_deck(DeckType.Hermit), current_choice=default_choice, loaded_effect=Effect(type=EffectType.Nothing, val=0))
