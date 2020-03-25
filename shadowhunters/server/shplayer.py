import requests, json, time, click
from threading import Thread
import signal
import sys

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
    def __init__(self, gameid, name):
        self.gameid = gameid
        self.name = name
        self.running = False
        self.uuid = ""
        self.data = {}
        self.last_phase = ""

    def join_game(self):
        url = "http://127.0.0.1:8000/games/{0}/players?name={1}".format(self.gameid, self.name)
        payload = {}
        headers= {}
        response = requests.request("POST", url, headers=headers, data = payload)
        response = json.loads(response.text.encode('utf8'))
        print(response)
        self.uuid = response["uuid"]

    def get_game_data(self):
        url = "http://127.0.0.1:8000/games/{0}".format(self.gameid)
        payload = {}
        headers= {}
        response = requests.request("GET", url, headers=headers, data = payload)
        response = json.loads(response.text.encode('utf8'))
        self.data = response
        if self.last_phase != self.data["phase"]:
            print(self.data["players"][self.uuid])
            print(self.data["notifications"])
        self.last_phase = self.data["phase"]

    def start_game(self):
        url = "http://127.0.0.1:8000/games/{0}/start".format(self.gameid)
        payload = {}
        headers= {}
        response = requests.request("POST", url, headers=headers, data = payload)
        response = json.loads(response.text.encode('utf8'))

    def roll(self):
        url = "http://127.0.0.1:8000/games/{0}/players/{1}/roll".format(self.gameid, self.uuid)
        payload = {}
        headers= {}
        response = requests.request("POST", url, headers=headers, data = payload)
        response = json.loads(response.text.encode('utf8'))

    def roll_target(self, location):
        url = "http://127.0.0.1:8000/games/{0}/players/{1}/roll_target".format(self.gameid, self.uuid)
        print(location)
        payload = json.dumps(location)
        headers= {}
        response = requests.request("POST", url, headers=headers, data = payload)
        response = json.loads(response.text.encode('utf8'))

    def update(self):
        # Get game state
        self.get_game_data()

        # If it is my turn, do something
        if self.data["turn"] == self.uuid:
            if self.data["phase"] == "roll":
                self.roll()
            elif self.data["phase"] == "roll_target":
                # Pick where to go!
                self.roll_target(self.data["locations"][0])

    def run(self):
        self.running = True
        while self.running:
            self.update()
            #time.sleep(0.05)

def new_game():
    url = "http://127.0.0.1:8000/games"
    payload = {}
    headers= {}
    response = requests.request("POST", url, headers=headers, data = payload)
    response = json.loads(response.text.encode('utf8'))
    return response

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
        gameid = new_game()["uuid"]
        p1 = player_thread(gameid, "Player 1")
        p2 = player_thread(gameid, "Player 2")
        p3 = player_thread(gameid, "Player 3")
        p4 = player_thread(gameid, "Player 4")
        p5 = player_thread(gameid, "Player 5")
        p6 = player_thread(gameid, "Player 6")
        p7 = player_thread(gameid, "Player 7")
        p8 = player_thread(gameid, "Player 8")

        p1.start()
        p2.start()
        p3.start()
        p4.start()
        p5.start()
        p6.start()
        p7.start()
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
        gameid = new_game()["uuid"]
        print("Created a new game with UUID: {}".format(gameid))
    
    if gameid is not None:
        player = SHPlayer(gameid, name)
        player.join_game()
        player.run()
    else:
        print("Please specify GAMEID or use --new flag")
        exit()

if __name__ == "__main__":
    main(None, None, None, None)