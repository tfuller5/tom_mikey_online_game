from __future__ import print_function
from time import sleep

from accessible_output2.outputs.auto import Auto
output = Auto()

from PodSixNet.Connection import connection, ConnectionListener

from _thread import *
from game_bit import mainloop, youmove
import pygame
import simple_menu
from chat import chatbox


class Client(ConnectionListener):
    def __init__(self):
        self.name = load_nickname()

    def connect(self, host, port):
        self.Connect((host, port))

        connection.Send({"action": "give_nickname", "name": self.name})
        t = start_new_thread(lambda *args: mainloop(self), ())
        self.Loop()

    def Save(self, encrypted_data):
        connection.Send({"action": "save_player_data", "data": encrypted_data})

    def ListEveryone(self):
        connection.Send({"action": "ListEveryone"})

    def Network_ListEveryone(self, data):
        ps = data["names"]
        output.speak("There are " + str(len(ps)) + " players in the server")
        for p in ps:
            output.speak(f"{p}, what a great guy")

    def i_just_moved(self, x, y):
        connection.Send({"action": "i_just_moved", "x": x, "y": y})

    def Network_someone_just_moved(self, data):
        youmove(data["x"], data["y"])

    def Chat(self, message):
        output.speak("You said: "+ message)
        connection.Send({"action": "chat", "message": message})


    def Network_chat(self, data):
        output.speak(data["name"] + " said " + data["message"])

    def Network_confirmation(self, data):
        output.speak(f"CONFIRMATION. <{data['response']}>")
        print(f"CONFIRMATION. <{data['response']}>")

    def Network_new_guy(self, data):
        output.speak(data["name"] + " has connected to the server")

    def Network_someone_else_disconnected(self, data):
        output.speak(str(data["name"]) + " has disconnected from the server")

    def Loop(self):
        connection.Pump()
        self.Pump()


host = "81.106.228.102"
host = "44.200.50.168"
host = "34.205.4.43"
port = 8080


def load_nickname():
    nickname_file = "game_files/nick_is_the_name.txt"

    try:
        file = open(nickname_file, "r")
        nick = file.read()
        file.close()
        return nick
    except FileNotFoundError:
        open(nickname_file, "w").close()
        return None

def get_nickname():
    nickname_box = chatbox()
    nickname_box.activate()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                name = nickname_box.send_key(event)
                if name:
                    if name.isalnum():
                        name = name.replace(" ", "_")
                        file = open("game_files/nick_is_the_name.txt", "w")
                        file.write(name)
                        file.close()
                        return name
                    else:
                        output.speak("bad name")
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

def menu(client):
    s = simple_menu.simple_menu(clicksound="menuclick.ogg", edgesound="menuedge.ogg", entersound="menuenter.ogg",wrapsound="menuwrap.ogg", leftright=False, updown=True, wrapping=True, homeend=True)

    s.add_item("Join as new player", "new")
    if client.name:
        s.add_item(f"Join as {client.name}", "old")

    choice = s.run(f"Welcome to a game, this is a game", True)

    print(choice)
    if s.get_item_name(choice) == "new":
        client.name = get_nickname()


pygame.init()
pygame.display.set_mode([50, 50])
c = Client()

menu(c)

c.connect(host, port)

while True:
    c.Loop()
    sleep(0.001)
