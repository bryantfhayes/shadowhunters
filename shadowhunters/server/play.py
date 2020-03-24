import requests, json, time, curses

class SHClient():
    def __init__(self):
        self.data = {}

    def new_game(self):
        url = "http://127.0.0.1:8000/games"
        payload = {}
        headers= {}
        response = requests.request("POST", url, headers=headers, data = payload)
        response = json.loads(response.text.encode('utf8'))
        self.data = response
        self.playerdata = []

    def add_player(self, name):
        url = "http://127.0.0.1:8000/games/{0}/players?name={1}".format(self.data["uuid"], name)
        payload = {}
        headers= {}
        response = requests.request("POST", url, headers=headers, data = payload)
        response = json.loads(response.text.encode('utf8'))
        self.playerdata.append(response)

    def start(self):
        url = "http://127.0.0.1:8000/games/{0}/start".format(self.data["uuid"])
        payload = {}
        headers= {}
        response = requests.request("POST", url, headers=headers, data = payload)
        response = json.loads(response.text.encode('utf8'))
        print(response)

    def get_game(self):
        url = "http://127.0.0.1:8000/games/{0}".format(self.data["uuid"])
        payload = {}
        headers= {}
        response = requests.request("GET", url, headers=headers, data = payload)
        response = json.loads(response.text.encode('utf8'))
        print(response)

shc = SHClient()
shc.new_game()
shc.add_player("player-1")
shc.add_player("player-2")
shc.add_player("player-3")
shc.add_player("player-4")
shc.start()
shc.get_game()
