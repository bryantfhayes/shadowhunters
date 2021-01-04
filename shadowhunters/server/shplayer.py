import requests, json, time, click

from model import Game, Role, Equipment, Location, Deck, Player, Phase, LocationAction, Choice, ChoiceType
from threading import Thread

import signal
import sys
import random

p1, p2, p3, p4 = None, None, None, None
p5, p6, p7, p8 = None, None, None, None


def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    p1.running = False
    p2.running = False
    p3.running = False
    p4.running = False
    p5.running = False
    p6.running = False
    p7.running = False
    p8.running = False

signal.signal(signal.SIGINT, signal_handler)

class SHPlayer(object):

    # Static Class Variables
    SERVER_URL = "http://127.0.0.1:8000"

    def __init__(self, gameid, name):
        self.gameid = gameid
        self.name = name
        self.running = False
        self.uuid = ""
        self.data = {}
        self.last_phase = ""
        self.game = None

    @classmethod
    def send_message(self, endpoint, httptype="POST", payload={}, headers={}):
        """
        Helper function to send POST/GET commands
        """
        response = requests.request(httptype, SHPlayer.SERVER_URL + endpoint, headers=headers, data=payload)
        response = json.loads(response.text.encode('utf8'))
        return response

    @classmethod
    def new_game(self):
        response = self.send_message("/games")
        return response

    def join_game(self):
        """
        Join game
        """
        response = self.send_message("/games/{0}/players?name={1}".format(self.gameid, self.name))
        player = Player(**response)
        self.uuid = player.uuid

    def get_game_data(self):   
        """
        Get the current game state
        """     
        response = self.send_message("/games/{0}".format(self.gameid), httptype="GET")
        self.game = Game(**response)
        if self.last_phase != self.game.phase:
            print(self.game.players[self.uuid])
            print(self.game.notifications)
        self.last_phase = self.game.phase

    def start_game(self):
        """
        Start the game!
        """
        self.send_message("/games/{0}/start".format(self.gameid))

    def do_roll(self):
        """
        Attempt to roll the dice
        """
        self.send_message("/games/{0}/players/{1}/roll".format(self.gameid, self.uuid))
        
    def do_roll_target(self, location):
        """
        Player rolled a 7, time to choose where to go
        """
        self.send_message("/games/{0}/players/{1}/roll_target".format(self.gameid, self.uuid), payload=json.dumps(location.dict()))
    
    def do_action(self):
        """
        Player decides to use the location-based action.

        For example: They will call this end point if they are
                     on the cemetery and decide to draw a card.
        """
        self.send_message("/games/{0}/players/{1}/action".format(self.gameid, self.uuid))

    def do_action_target(self):
        """
        Player decides how to respond to awaiting action. The action requires a target of some kind.
        For example: you landed on Weird Woods and you need to select a target.
        """
        print("Current Event: {}".format(self.game.action_results))
        if self.game.action_results.location_action == LocationAction.DrawAny:
            target = "blackdeck"
            self.send_message("/games/{0}/players/{1}/action_target_deck/{2}".format(self.gameid, self.uuid, target))
        else:
            target = random.choice(list(self.game.players.values())).uuid
            print(target)
            self.send_message("/games/{0}/players/{1}/action_target_player/{2}".format(self.gameid, self.uuid, target))

    def choice_needed(self):
        print(self.game.current_choice)
        choice_idx = 0
        self.send_message("/games/{0}/players/{1}/choice/{2}".format(self.gameid, self.uuid, choice_idx))

    def endturn(self):
        self.send_message("/games/{0}/players/{1}/endturn".format(self.gameid, self.uuid))

    def update(self):
        """
        Main update loop
        """
        # Get game state
        self.get_game_data()

        # If it is my turn, do something
        if self.game.turn == self.uuid:

            print(self.game.phase)

            if self.game.phase == Phase.Roll:
                # Tell the server to roll the dice
                self.do_roll()
            elif self.game.phase == Phase.ChoiceNeeded:
                self.choice_needed()
            elif self.game.phase == Phase.RollTarget:
                # Tell the server where you want to go
                self.do_roll_target(self.game.locations[0])
            elif self.game.phase == Phase.Action:
                # Ask server to perform an action based on the location you are at
                self.do_action()
            elif self.game.phase == Phase.ActionTarget:
                # Tell server which action you want to perform since it is waiting for your choice
                self.do_action_target()
            else:
                self.endturn()

class player_thread(Thread):
    def __init__(self, gameid, name):
        Thread.__init__(self)
        self.gameid = gameid
        self.name = name
        self.running = True
        self.start_game = False

    def run(self):
        player = SHPlayer(self.gameid, self.name)
        player.join_game()
        
        while self.running:
            time.sleep(0.5)
            player.update()

            if self.start_game:
                self.start_game = False
                player.start_game()

@click.command()
@click.option('--gameid', help='The ID of the game you wish to join')
@click.option('--name', help='The name others will see you as')
@click.option('--new', is_flag=True, help='Start a new game')
@click.option('--test', is_flag=True, help='Test a game with 4 players')
def main(gameid, name, new, test):
    global p1, p2, p3, p4, p5, p6, p7, p8
    if test:
        gameid = Game(**SHPlayer.new_game()).uuid
        p1 = player_thread(gameid, "Player 1")
        p2 = player_thread(gameid, "Player 2")
        p3 = player_thread(gameid, "Player 3")
        p4 = player_thread(gameid, "Player 4")
        p5 = player_thread(gameid, "Player 5")
        p6 = player_thread(gameid, "Player 6")
        p7 = player_thread(gameid, "Player 7")
        p8 = player_thread(gameid, "Player 8")

        p1.start()
        time.sleep(0.35)
        p2.start()
        time.sleep(0.35)
        p3.start()
        time.sleep(0.35)
        p4.start()
        time.sleep(0.35)
        p5.start()
        time.sleep(0.35)
        p6.start()
        time.sleep(0.35)
        p7.start()
        time.sleep(0.35)
        p8.start()

        p8.start_game = True

        p1.join()
        p2.join()
        p3.join()
        p4.join()
        p5.join()
        p6.join()
        p7.join()
        p8.join()

        sys.exit(0)
    
    if new:
        gameid = Game(**SHPlayer.new_game()).uuid
        print("Created a new game with UUID: {}".format(gameid))
    
    if gameid is not None:
        player = SHPlayer(gameid, name)
        player.join_game()
    else:
        print("Please specify GAMEID or use --new flag")
        exit()

if __name__ == "__main__":
    main(None, None, None, None)